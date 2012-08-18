#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from apps.main.decorators import check_battle
from apps.main.models import Hero, BattleQueue, Battle
import datetime


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

def rating(request):

    return render(request, 'main/rating.html',{})


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
        #opponent exists, start battle
        battle = Battle(
            hero1=request.user.hero,
            hero2=opponent,
            date=datetime.datetime.now(),
            is_active=True
        )
        battle.save()
        BattleQueue.objects.filter(hero__in=[request.user.hero, opponent]).delete()

        return redirect('battle')
    except Exception:
        pass



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
    return render(request, 'main/battle.html',{'hero':request.user.hero})

@login_required
@check_battle
def postbattle(request):
    return render(request, 'main/postbattle.html',{'hero':request.user.hero})