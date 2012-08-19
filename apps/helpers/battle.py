# coding: utf-8
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from apps.helpers.formulas import get_hit_chance, is_hits, get_damage, get_exp
from apps.main.models import Unit, HeroEffect, UnitEffect, CastingSpell, HeroLog, Spell

def check_defeat(army):
    """ Checks defeat of hero in battle or not. Hero defeated if his army is defeated"""
    return all([unit.life <= 0 for unit in army])

def battle_result_hero_defeated(battle, hero, opponent, opponent_defeated):
    """ Ends battle with loosing of one or more heroes"""

    battle.add_log_line_hero_defeated( hero.login)

    if not opponent_defeated:
        battle.winner = opponent

        opponent.wins += 1
        opponent.add_experience(get_exp(opponent, hero, True))
    else:
        opponent.losses += 1
        opponent.add_experience(get_exp(opponent, hero, False))
        battle.add_log_line_hero_defeated( opponent.login)

    hero.losses +=1
    hero.add_experience(get_exp(hero, opponent, False))

    hero.save()
    opponent.save()

    battle.is_active = False
    battle.save()


def process_move(battle, hero1, hero2, hero1_army, hero2_army):
    """ Calcs result of move """
    army_dict = dict([(unit.pk,unit) for unit in hero1_army+hero2_army])
    #casting of spells must be before direct attacks
    # only units survived after spells do attack
    try:
        spell1 = CastingSpell.objects.filter(spell__hero=hero1)[0]
        target1 = spell1.target_unit if spell1.target_unit is not None else spell1.target_hero
        buf1 = spell1.spell.produces_effect()
        if buf1 and not buf2:
            spell1.spell.cast(hero1, hero1_army, hero2, hero2_army, target1, spell1.target_param)
        else:
        # cases of both instants, both bufs and inverse of first case are at this branch
            spell1.spell.cast(hero1, hero1_army, hero2, hero2_army, target1, spell1.target_param)
    except Exception:
        pass

    try:
        spell2 = CastingSpell.objects.filter(spell__hero=hero2)[0]
        target2 = spell2.target_unit if spell2.target_unit is not None else spell2.target_hero

        buf2 = spell2.spell.produces_effect()
        # bufs should be processed before instants since
        # the former can supply unit with immunity
        if buf1 and not buf2:
            spell2.spell.cast(hero2, hero2_army, hero1, hero1_army, target2, spell2.target_param)
        else:
            # cases of both instants, both bufs and inverse of first case are at this branch
            spell2.spell.cast(hero2, hero2_army, hero1, hero1_army, target2, spell2.target_param)
    except Exception:
        pass

    # after casting delete empty entries from spellbook
    Spell.objects.filter(cnt__lte=0).delete()
    # and delete what was casted at this turn
    CastingSpell.objects.filter(Q(spell__hero=hero1)|Q(spell__hero=hero2)).delete()

    defeated_units = []
    for unit in hero1_army+hero2_army:
        target = army_dict[unit.battle_target_id]
        if target.life<=0:
            continue
        if is_hits(unit.get_attack(), target.get_defence()):
            damage = get_damage(unit.get_attack(), target.get_defence())
            target.life -= damage
            battle.add_log_line_hits(unit.custom_name, target.custom_name, damage)
            if target.life<=0:
                defeated_units.append(target)
            target.changed = True
        else:
            battle.add_log_line_missing(unit.custom_name, target.custom_name)

    for unit in defeated_units:
        battle.add_log_line_unit_defeated(unit.custom_name)


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
        battle.add_log_line_new_round()
        battle.save()
        Unit.objects.filter(Q(hero=hero1)|Q(hero=hero2)).update(battle_target=None)
        # decreasing duration of effects and eliminating ones that ended
        HeroEffect.objects.filter(Q(hero=hero1)|Q(hero=hero2)).update(duration=F('duration')-1)
        HeroEffect.objects.filter(duration__lte=0).delete()
        UnitEffect.objects.filter(unit__in=(hero1.units.filter(life_gt=0)|hero2.units.filter(life_gt=0))).update(duration=F('duration')-1)
        UnitEffect.objects.filter(duration__lte=0).delete()
        for unit in hero1_army+hero2_army:
            if hasattr(unit, 'changed'):
                unit.save()

        hero1_army = [unit for unit in hero1_army if unit.life>0]
        hero2_army = [unit for unit in hero2_army if unit.life>0]

        #CastingSpell.objects.select_related().filter(spell__in=(hero1.spells.all()|hero2.spells.all())).delete()

