#coding: utf-8
from __future__ import division

from math import ceil, floor
import random
import math

def dsu(level):
    """ Returns experince needed to reach next level.
    
    `level` is *current* level of a hero.
    """
    return level*10

def get_hit_chance(attack, defence, missRequired=True):
    """ Computes hit chance [0..1] based on attack and defence stat """
    chance = 1
    if attack>=defence:
        if missRequired:
            chance = 0.95
    else:
        chance = attack/defence
    if chance<0.05:
        chance = 0.05
    return chance

def is_hits(attack, defence, missRequired=True):
    """Check hits one unit another, or not"""
    return random.random()<=get_hit_chance(attack, defence, missRequired)



def get_damage(attack, defence):
    """ Returns damaged based on attack and defence stat values """
    if attack>=defence:
        if defence==0:
            ratio = 2
        else:
            ratio = 1+(attack-defence)*0.5/defence
        if ratio > 1.5:
            ratio = 1.5
    else:
        ratio = (attack+(defence-attack)*0.5)/defence
    if ratio<0.25:
        ratio = 0.25
    dmg = int(attack*ratio)
    return 1 if dmg<1 else dmg

def get_exp(hero, opponent, win = True):
    """ Returns experience hero gained in battle """
    if win:
        return min(10, int(2*opponent.get_total_power()/hero.get_total_power()))
    else:
        return 0 if opponent.get_total_power() < hero.get_total_power() else 1

def get_spell_duration(level, attentiveness):
    return int(1.5*math.ceil(0.1*level))+int(attentiveness*0.1)

def scale_prop(prop, prop_limit, prop_max=16000):
    """ Scales down account and repos properties.

    Returns new value of the scaled down property.
    """
    lim = prop_limit
    if prop < lim:
        return prop
    ratio = (prop-lim)/(prop_max-lim)
    if prop < lim+(prop_max-lim)/2:
        ratio = (prop-lim)/((prop_max-lim)/2)
    new_prop = int(ratio*lim)
    return 1 if new_prop < 1 else new_prop

def lang_to_race(lang):
    """ Returns race based on repo language """
    LANG_TO_RACES = {
        'Python': 'elf',
        'Ruby': 'goblin',
        'PHP': 'ork',
        'JavaScript': 'halfing',
        'CoffeeScript': 'halfing',
        'Objective-C': 'troll',
        'Java': 'titan',
        'Scala': 'titan',
        'C++': 'gnome',
        'C': 'dwarf'
    }
    if lang in LANG_TO_RACES:
        return LANG_TO_RACES[lang]
    else:
        return 'human'


def race_bonuses(race, level=1):
    """ Returns stat bonuses based on race and level of hero """
    BONUSES = {
        'troll': (0, 2, 2, 0),
        'goblin': (2, 1, 1, 0),
        'halfing': (2, 0, 2, 0),
        'elf': (0, 0, 2, 2),
        'titan': (1, 0, 1, 2),
        'ork': (2, 2, 0, 0),
        'dwarf': (1, 2, 1, 0),
        'human': (1, 1, 1, 1),
        'gnome': (0, 1, 1, 2)
    }
    bonus = (1,1,1,1)
    if race in BONUSES:
        bonus = BONUSES[race]
    LM = ceil(0.1*level)
    bonus = [int(stat*LM) for stat in  bonus]
    return {
        'attack': bonus[0],
        'defence': bonus[1],
        'charm': bonus[2],
        'attentiveness': bonus[3],
    }
