from django.shortcuts import redirect

def check_battle(func):
    def wrapper(request,*args, **kwargs):
        if request.user.hero.in_battle():
            return redirect('battle')
        else:
            return func(*args, **kwargs)
    return wrapper