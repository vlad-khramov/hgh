from django.db.models.query_utils import Q
from apps.helpers.formulas import get_hit_chance, is_hits, get_damage, get_exp
from apps.main.models import Unit

def check_defeat(army):
    """ Checks defeat of hero in battle or not. Hero defeated if his army is defeated"""
    for unit in army:
        if unit.life > 0:
            return False
            break
    return True

def battle_result_hero_defeated(battle, hero, opponent, opponent_defeated):
    """ Ends battle with loosing of one or more heroes"""
    if not opponent_defeated:
        battle.winner = opponent

        opponent.wins += 1
        opponent.experience += get_exp(opponent, hero, True)
    else:
        opponent.losses += 1
        opponent.experience += get_exp(opponent, hero, False)

    hero.losses +=1
    hero.experience += get_exp(hero, opponent, False)
    if hero.has_got_level():
        hero.gain_level()
    if opponent.has_got_level():
        opponent.gain_level()

    hero.save()
    opponent.save()

    battle.is_active = False
    battle.save()


def process_move(battle, hero1, hero2, hero1_army, hero2_army):
    """ Calcs result of move """
    army_dict = dict([(unit.pk,unit) for unit in hero1_army+hero2_army])


    for unit in hero1_army+hero2_army:
        target = army_dict[unit.battle_target_id]
        if is_hits(unit.get_attack(), target.get_defence()):
            target.life -= get_damage(unit.get_attack(), target.get_defence())
            target.changed = True


    hero1_defeated = check_defeat(hero1_army)
    hero2_defeated = check_defeat(hero2_army)

    if hero1_defeated:
        battle_result_hero_defeated(battle, hero1, hero2, hero2_defeated)
    elif hero2_defeated:
        battle_result_hero_defeated(battle, hero2, hero1, hero1_defeated)
    else:
        battle.round += 1
        battle.hero1_moved = False
        battle.hero2_moved = False
        battle.save()
        Unit.objects.filter(Q(hero=hero1)|Q(hero=hero2)).update(battle_target=None)
        for unit in hero1_army+hero2_army:
            if hasattr(unit, 'changed'):
                unit.save()



