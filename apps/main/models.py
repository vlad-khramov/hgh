#coding: utf-8
import datetime
from django.contrib.auth.models import User
from django.db import models
import math
import operator
from social_auth.backends.contrib.github import GithubBackend
from social_auth.signals import pre_update
from apps.helpers import gh, formulas

class Hero(models.Model):
    """Hero, based on github account of user"""
    user = models.OneToOneField(User, related_name='hero')

    login = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='')

    avatar_url = models.URLField(default='')
    html_url = models.URLField(default='')
    blog = models.URLField(default='')
    location = models.CharField(max_length=200,default='')
    hireable = models.BooleanField(default=False)

    public_repos = models.IntegerField(default=0)
    public_gists = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    attack_github = models.IntegerField(default=0)
    defence_github = models.IntegerField(default=0)
    attentiveness_github = models.IntegerField(default=0)
    charm_github = models.IntegerField(default=0)

    attack_own = models.IntegerField(default=0)
    defence_own = models.IntegerField(default=0)
    attentiveness_own = models.IntegerField(default=0)
    charm_own = models.IntegerField(default=0)

    race = models.CharField(max_length=100, default='')

    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)

    last_update = models.DateTimeField(default=datetime.datetime(2000,1,1))

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

    def update_from_response(self, response):
        """updates hero with info from auth response"""
        for key, val in response.items():
            if key != 'id' and not val is None  and hasattr(self, key):
                setattr(self, key, val)

    def update_race(self):
        """updates race of hero (most popular race from units)"""
        if self.race: return

        if Unit.objects.filter(hero=self).count()==0:
            self.race = 'human'

        units = Unit.objects.filter(hero=self)

        races = dict()
        for unit in units:
            if unit.race in races:
                races[unit.race] += 1
            else:
                races[unit.race] = 1

        self.race = sorted(races.iteritems(), key=lambda (k,v): (v,k))[0][0]
        self.save()




    def update_army(self):
        """
        updates army of hero with info of repositories in github
        if user hasn't repository, he get a unit Dummy
        """
        #todo: check for battle
        repos = gh.get_repos(self.login)
        if not repos:
            if Unit.objects.filter(hero=self).count()>0:
                return
            else:
                Unit(hero=self, name = 'Dummy').save()
                return

        Unit.objects.filter(hero=self).delete()

        for repo in repos:
            unit = Unit(hero=self)
            unit.update_from_response(repo)
            unit.save()


    def save(self, *args, **kwargs):
        self.attack_github = 1 + math.ceil(self.public_repos/2.0) + math.ceil(self.followers/2.0)
        self.defence_github = self.public_repos + math.ceil(self.public_gists/2.0)
        self.attentiveness_github = 1 + self.following + math.ceil(self.followers/2.0)
        self.charm_github = self.followers + (1 if self.hireable else 0)

        super(Hero, self).save(*args, **kwargs)


class Unit(models.Model):
    """member of army of hero, based on repositories of user"""

    hero = models.ForeignKey(Hero, related_name='units')

    name = models.CharField(max_length=200)
    custom_name = models.CharField(max_length=200)

    html_url = models.URLField(default='')
    language = models.CharField(max_length=100, default='')

    forks = models.IntegerField(default=0)
    watchers = models.IntegerField(default=0)
    open_issues = models.IntegerField(default=0)

    race = models.CharField(max_length=100, default='human')

    attack_github = models.IntegerField(default=0)
    defence_github = models.IntegerField(default=0)
    attentiveness_github = models.IntegerField(default=0)
    charm_github = models.IntegerField(default=0)

    def _get_stat(self, stat):
        """returns total value of stat by its name"""
        return getattr(self, stat+'_github') + getattr(self.hero, 'get_'+stat)()

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


    def update_from_response(self, response):
        """updates hero with info from auth response"""
        for key, val in response.items():
            if key != 'id' and not val is None and hasattr(self, key):
                setattr(self, key, val)

    def save(self, *args, **kwargs):
        self.attack_github = math.ceil(self.forks/2.0)
        self.defence_github = self.forks + math.ceil(self.watchers/4.0)
        self.attentiveness_github = math.ceil(self.watchers/2.0)
        self.charm_github = math.ceil(self.watchers/2.0) + math.ceil(self.open_issues/4.0)

        self.race = formulas.lang_to_race(self.language)

        super(Unit, self).save(*args, **kwargs)

class Spell(models.Model):
    """a spell that `hero` can cast"""

    hero = models.ForeignKey(Hero, related_name='spells')

    type = models.CharField(max_length=200)
    cnt = models.IntegerField(default=1)
    



def social_auth_update_user(sender, user, response, details, **kwargs):

    try:
        hero = Hero.objects.get(user=user)
        created = False
    except Exception:
        hero = Hero(user=user)
        created = True

    hero.update_from_response(response)
    hero.save()

    if created:
        hero.update_army()
        hero.update_race()


    return True

pre_update.connect(social_auth_update_user, sender=GithubBackend)

