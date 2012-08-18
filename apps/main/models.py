#coding: utf-8
from django.contrib.auth.models import User
from django.db import models

class Hero(models.Model):
    user = models.ForeignKey(User)

    avatar_url = models.URLField()
    html_url = models.URLField()
    blog = models.URLField()
    location = models.CharField(max_length=200)
    hireable = models.BooleanField()

    public_repos = models.IntegerField()
    public_gists = models.IntegerField()
    followers = models.IntegerField()
    following = models.IntegerField()

    attack_github = models.IntegerField()
    defence_github = models.IntegerField()
    attentiveness_github = models.IntegerField()
    charm_github = models.IntegerField()

    attack_own = models.IntegerField()
    defence_own = models.IntegerField()
    attentiveness_own = models.IntegerField()
    charm_own = models.IntegerField()

    race = models.CharField(max_length=100)

    wins = models.IntegerField()
    losses = models.IntegerField()
    experience = models.IntegerField()

    last_update = models.CharField(max_length=100)
