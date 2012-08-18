from django.test import TestCase
from apps.main.models import Hero, Unit


class SimpleTest(TestCase):

    def test_hero_stats(self):
        """
        tests correct getting stats of hero
        """
        hero = Hero(
            attack_github = 2,
            attack_own = 3
        )
        assert hero.get_attack() == 5


    def test_unit_stats(self):
        """
        tests correct getting stats of hero
        """
        hero = Hero(
            attack_github = 2,
            attack_own = 3
        )
        unit = Unit(
            hero = hero,
            attack_github = 4
        )

        assert unit.get_attack() == 9



    def test_hero_update_race(self):
        """tests setting race based on race of units"""
        hero = Hero()
        Unit(hero=hero,race='human')
        Unit(hero=hero,race='elf')
        Unit(hero=hero,race='elf')

        hero.update_race()
        print hero.race

        assert hero.race == 'elf'


