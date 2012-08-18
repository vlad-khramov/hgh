#coding: utf-8
from django.contrib.auth.models import User
from django.db import models

class Hero(models.Model):
    """Hero, based on github account of user"""
    user = models.ForeignKey(User)

    login = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

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

    def _get_stat(self, stat):
        """returns total value of stat by its name"""
        return getattr(self, stat+'_own')+getattr(self, stat+'_github')

    def get_attack(self):
        """returns total hero attack"""
        return self._get_stat('attack')

    def get_defence(self):
        """returns total hero defence"""
        return self._get_stat('defence')

    def get_attentiveness(self):
        """returns total hero attentiveness"""
        return self._get_stat('attentiveness')

    def get_charm(self):
        """returns total hero charm"""
        return self._get_stat('charm')


class Unit(models.Model):
    """member of army of hero, based on repositories of user"""

    hero = models.ForeignKey(Hero, related_name='units')

    name = models.CharField(max_length=200)
    custom_name = models.CharField(max_length=200)

    html_url = models.URLField()
    language = models.CharField(max_length=100)

    forks = models.IntegerField()
    watchers = models.IntegerField()
    open_issues = models.IntegerField()

    race = models.CharField(max_length=100)

    attack_github = models.IntegerField()
    defence_github = models.IntegerField()
    attentiveness_github = models.IntegerField()
    charm_github = models.IntegerField()