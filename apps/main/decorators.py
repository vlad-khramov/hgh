# coding: utf-8
from django.shortcuts import redirect

def check_battle(func):
    def wrapper(request,*args, **kwargs):
        if request.user.hero.get_battle():
            return redirect('battle')
        else:
            return func(request,*args, **kwargs)
    return wrapper