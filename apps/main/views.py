#coding: utf-8
import random
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from apps.helpers.battle import process_move
from apps.main.decorators import check_battle
from apps.main.models import Hero, BattleQueue, Battle, Unit
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
    return render(request, 'main/profile.html',{'hero':request.user.hero})

def info(request, login=''):
    hero = get_object_or_404(Hero, login=login)
    return render(request, 'main/info.html', {'hero': hero})

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
        battle.save()
        for unit in Unit.objects.filter(Q(hero=request.user.hero)|Q(hero=opponent)):
            unit.life = unit.get_max_life()

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
    battle = request.user.hero.get_battle()
    hero = request.user.hero
    army = hero.units.select_related()
    army_dict = dict([(unit.pk,unit) for unit in army])

    opponent = battle.get_opponent(hero)
    opponent_army = opponent.units.select_related()
    opponent_army_dict = dict([(unit.pk,unit) for unit in opponent_army])

    if battle is None:
        return redirect('profile')

    if 'runaway' in request.GET:
        battle.is_active=False
        battle.winner = battle.get_opponent(hero)
        battle.save()

        return redirect('profile')

    is_moved = battle.is_moved(hero)

    if 'move' in request.POST and not is_moved:
        for unit in army:
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

    if battle.hero1_moved and battle.hero1_moved:
        process_move(battle, hero, opponent, army, opponent_army)





    return render(request, 'main/battle.html', {
        'hero': hero,
        'army': army,
        'is_moved': is_moved,

        'opponent': opponent,
        'opponent_army': opponent_army
    })

@login_required
@check_battle
def postbattle(request):
    return render(request, 'main/postbattle.html',{'hero':request.user.hero})