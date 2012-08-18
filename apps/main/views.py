#coding: utf-8
from django.shortcuts import render
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