#coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from apps.main.models import Hero, BattleQueue
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

def profile(request):
    return render(request, 'main/profile.html',{'hero':request.user.hero})

def info(request, login=''):
    hero = get_object_or_404(Hero, login=login)
    return render(request, 'main/info.html', {'hero': hero})


def prebattle(request):

    return render(request, 'main/prebattle.html', {})

def battle(request):
    return render(request, 'main/battle.html',{'hero':request.user.hero})

def postbattle(request):
    return render(request, 'main/postbattle.html',{'hero':request.user.hero})