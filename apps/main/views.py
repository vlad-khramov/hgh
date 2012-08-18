#coding: utf-8
from django.shortcuts import render


def home(request):

    return render(request, 'main/home.html',{})


def login(request):

    return render(request, 'main/login.html',{})

def rating(request):

    return render(request, 'main/rating.html',{})