# coding: utf-8
import random
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import simplejson
from apps.helpers.battle import process_move
from apps.main.decorators import check_battle
from apps.main.models import Hero, BattleQueue, Battle, Unit, Spell, CastingSpell
import datetime
from apps.simplepagination import simple_paginate


def home(request):

    rating_exp = Hero.objects.order_by('-experience')[:20]
    rating_power = Hero.objects.extra(
        select={'total_power':'power + army_power'},
        order_by=('-total_power',)
    )[:20]

    return render(request, 'main/home.html',{
        'rating_exp': rating_exp,
        'rating_power': rating_power,

    })


def login(request):

    return render(request, 'main/login.html',{})

def login_error(request):

    return render(request, 'main/login_error.html',{})


def rating(request, type=''):

    if type=='experience':
        heroes = Hero.objects.order_by('-experience')
    elif type=='power':
        heroes = Hero.objects.extra(
            select={'total_power':'power + army_power'},
            order_by=('-total_power',)
        )
    else:
        raise Http404

    paginator = simple_paginate(heroes, request, style='digg')

    return render(request, 'main/rating.html', {
        'paginator': paginator,
        'type': type
    })


@login_required
@check_battle
def profile(request):
    return redirect('info', request.user.hero.login)

def info(request, login=''):
    hero = get_object_or_404(Hero, login=login)
    battles = list(hero.get_battles().select_related().order_by('-date')[:20])
    for battle in battles:
        battle.opponent = battle.get_opponent(hero)

    return render(request, 'main/info.html', {
        'hero': hero,
        'battles': battles
    })

@login_required
@check_battle
def prebattle(request):

    try:
        opponent = BattleQueue.objects.exclude(hero=request.user.hero)[0].hero
    except Exception:
        opponent = None

    if opponent: #opponent exists, start battle
        battle = Battle(
            hero1=request.user.hero,
            hero2=opponent,
            date=datetime.datetime.now(),
            is_active=True
        )
        battle.add_log_line_new_round()
        battle.save()
        for unit in Unit.objects.filter(Q(hero=request.user.hero)|Q(hero=opponent)):
            unit.life = unit.get_max_life()
            unit.battle_target=None
            unit.save()

        BattleQueue.objects.filter(hero__in=[request.user.hero, opponent]).delete()

        return redirect('battle')



    try:
        battle_queue = BattleQueue.objects.get(hero=request.user.hero)
    except Exception:
        battle_queue = BattleQueue(hero=request.user.hero, date=datetime.datetime.now())
        battle_queue.save()

    if 'cancel' in request.GET:
        battle_queue.delete()
        return redirect('profile')


    return render(request, 'main/prebattle.html', {})

@login_required
def battle(request):
    hero = request.user.hero
    battle = request.user.hero.get_battle()
    if battle is None:
        if Battle.objects.filter((Q(hero1=hero)&Q(hero1_seen_result=False))|(Q(hero2=hero)&Q(hero2_seen_result=False))).count()>0:
            return redirect('postbattle')
        else:
            return redirect('profile')

    army = list(hero.units.select_related().filter(life__gt = 0))

    opponent = battle.get_opponent(hero)
    opponent_army = list(opponent.units.select_related().filter(life__gt = 0))
    opponent_army_dict = dict([(unit.pk,unit) for unit in opponent_army])

    if battle is None:
        return redirect('profile')

    if 'runaway' in request.GET:
        battle.is_active=False
        battle.winner = battle.get_opponent(hero)
        battle.add_log_line_hero_runaway(hero.login)
        battle.save()

        return redirect('postbattle')

    is_moved = battle.is_moved(hero)

    if 'move' in request.POST and not is_moved:
        try:
            spell = Spell.objects.get(hero=hero, pk=request.POST['spell'])
        except Exception:
            spell = None #ignoring all reasons, why spell is empty (not selected, hacking attempt, etc)

        if spell:
            if spell.get_target_type()=='own_unit' \
                and 'param' in request.POST \
                and request.POST['param'] in ('attack','defence','attentiveness','charm'):
                try:
                    unit = Unit.objects.get(hero=hero,pk=request.POST['target'])
                    CastingSpell(spell=spell, target_unit=unit, target_param=request.POST['param']).save()
                except Exception:
                    pass
            if spell.get_target_type()=='hero'\
                and 'param' in request.POST\
                and request.POST['param'] in ('attack','defence','attentiveness','charm'):
                try:
                    CastingSpell(spell=spell, target_hero=hero, target_param=request.POST['param']).save()
                except Exception:
                    pass
            if spell.get_target_type()=='opponent_unit':
                try:
                    unit = Unit.objects.get(hero=opponent,pk=request.POST['target'])
                    CastingSpell(spell=spell, target_unit=unit).save()
                except Exception:
                    pass


        for unit in army:
            if unit.life<=0:
                continue
            try:
                target = int(request.POST['unit%s'%unit.pk])
            except Exception:
                target = 0

            if not target or not target in opponent_army_dict.keys():
                target = random.choice(opponent_army_dict.keys())

            unit.battle_target_id = target
            unit.save()

        battle.set_moved(hero, True)
        battle.save()
        is_moved = True

    if battle.hero1_moved and battle.hero2_moved:
        process_move(battle, hero, opponent, army, opponent_army)

    if not battle.is_active:
        return redirect('postbattle')

    spells = hero.spells.all()
    opponent_spells = opponent.spells.all()
    try:
        casted_spell = CastingSpell.objects.select_related().get(spell__in=spells)
        target = casted_spell.target_unit.custom_name if casted_spell.target_unit else casted_spell.target_hero.login
        param = casted_spell.target_param
        casted_spell = ("casted %s to %s" % (casted_spell.spell.type, target))\
                     + (' to param %s' % param if param else '')

    except Exception:
        casted_spell = ''

    return render(request, 'main/battle.html', {
        'hero': hero,
        'army': army,
        'spells': spells,
        'is_moved': is_moved,
        'casted_spell': casted_spell,

        'opponent': opponent,
        'opponent_army': opponent_army,
        'opponent_spells': opponent_spells,
        'battle': battle
    })

@login_required()
def get_target(request, id):
    """ Returns to js target and params for selected spell """
    hero = request.user.hero
    battle = hero.get_battle()
    if battle is None:
        raise Http404

    spell = get_object_or_404(Spell,hero=hero, pk=id)
    t_type = spell.get_target_type()
    result = dict()

    if t_type in ['hero']:
        result['target'] = {hero.pk:hero.login}
        result['param'] = {
            'attack':'attack',
            'defence':'defence',
            'attentiveness':'attentiveness',
            'charm':'charm'
        }
    if t_type in ['own_unit']:
        result['target'] = dict([(unit.pk,unit.custom_name) for unit in hero.units.filter(life__gt=0)])
        result['param'] = {
            'attack':'attack',
            'defence':'defence',
            'attentiveness':'attentiveness',
            'charm':'charm'
        }
    elif t_type in ['opponent_unit']:
        result['target'] = dict([(unit.pk,unit.custom_name) for unit in battle.get_opponent(hero).units.filter(life__gt=0)])
        result['param'] = {}

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')




@login_required
@check_battle
def postbattle(request):

    hero = request.user.hero
    try:
        battle = Battle.objects.filter((Q(hero1=hero)&Q(hero1_seen_result=False))|(Q(hero2=hero)&Q(hero2_seen_result=False)))[0]
    except Exception:
        return redirect('profile')

    if battle.winner == hero:
        result = 'won'
    else:
        result = 'lose'

    Battle.objects.filter(hero1=hero, hero1_seen_result=False).update(hero1_seen_result=True)
    Battle.objects.filter(hero2=hero, hero2_seen_result=False).update(hero2_seen_result=True)

    return render(request, 'main/postbattle.html', {
        'hero': hero,
        'result': result,
        'battle': battle
    })



def battle_info(request, id=0):
    battle = get_object_or_404(Battle.objects.select_related(), pk=id)

    return render(request, 'main/battle_info.html', {
        'battle': battle
    })