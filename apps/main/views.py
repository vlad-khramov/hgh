#coding: utf-8
from django.shortcuts import render, get_object_or_404
from apps.main.models import Hero


def home(request):

    rating_exp = Hero.objects.order_by('-experience')[:20]
    return render(request, 'main/home.html',{
        'rating_exp': rating_exp
    })


def login(request):

    return render(request, 'main/login.html',{})

def rating(request):

    return render(request, 'main/rating.html',{})

def profile(request):
    return render(request, 'main/profile.html',{'hero':request.user.hero})

def info(request, login=''):
    hero = get_object_or_404(Hero, login=login)
    return render(request, 'main/info.html', {'': hero})