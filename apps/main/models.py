#coding: utf-8
import datetime
from django.contrib.auth.models import User
from django.db import models
import math
from collections import Counter

from django.db.models.query_utils import Q
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
    level = models.IntegerField(default=1)

    power = models.IntegerField(default=0)
    army_power = models.IntegerField(default=0)
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

    def get_sum_stats(self):
        return self.get_attack()+self.get_defence()+self.get_attentiveness()+self.get_charm()

    def get_total_power(self):
        return self.power+self.army_power

    def in_battle_queue(self):
        return BattleQueue.objects.filter(hero=self).count() > 0

    def get_battle(self):
        try:
            return Battle.objects.get(Q(is_active=True),Q(hero1=self)|Q(hero2=self))
        except Exception:
            return None

    def update_from_response(self, response):
        """updates hero with info from auth response"""
        for key, val in response.items():
            if key != 'id' and not val is None  and hasattr(self, key):
                setattr(self, key, val)

    def update_race(self):
        """
        Updates race of hero (most popular race from units) and adds race bonuses.
        
        Race is set only once (after registration).
        """
        if self.race: return

        if Unit.objects.filter(hero=self).count()==0:
            self.race = 'human'
        else:
            units = Unit.objects.filter(hero=self)
            self.race = Counter(units).most_common()[0][0]
        for stat, value in formulas.race_bonuses(self.race).items():
            setattr(self, stat+'_own', getattr(self, stat+'_own')+value)


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
                self.army_power = 0
                return

        Unit.objects.filter(hero=self).delete()

        self.army_power = 0
        for repo in repos:
            unit = Unit(hero=self)
            unit.update_from_response(repo)
            unit.save()
            self.army_power += unit.get_sum_stats_github()


    def save(self, *args, **kwargs):
        self.attack_github = 1 + math.ceil(self.public_repos/2.0) + math.ceil(self.followers/2.0)
        self.defence_github = self.public_repos + math.ceil(self.public_gists/2.0)
        self.attentiveness_github = 1 + self.following + math.ceil(self.followers/2.0)
        self.charm_github = self.followers + (1 if self.hireable else 0)

        self.power = self.get_sum_stats()

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

    def get_sum_stats_github(self):
        return self.attack_github+self.defence_github+self.attentiveness_github+self.charm_github


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

        if not self.custom_name:
            self.custom_name = self.name

        super(Unit, self).save(*args, **kwargs)



class BattleQueue(models.Model):
    """Queue of heroes, waiting battle"""
    hero = models.ForeignKey(Hero)
    date = models.DateTimeField()

class Battle(models.Model):
    """battle betwen two heroes"""

    hero1 = models.ForeignKey(Hero, related_name='battles1')
    hero2 = models.ForeignKey(Hero, related_name='battles2')

    hero1_moved = models.BooleanField(default=False)
    hero2_moved = models.BooleanField(default=False)

    date = models.DateTimeField()

    is_active = models.BooleanField()
    round = models.SmallIntegerField(default=1)
    winner = models.ForeignKey(Hero, related_name='winned_battles', null=True, default=None)

    def get_opponent(self, hero):
        if self.hero1==hero:
            return self.hero2
        elif self.hero2==hero:
            return self.hero1
        else:
            return None




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
        hero.save()


    return True

pre_update.connect(social_auth_update_user, sender=GithubBackend)

