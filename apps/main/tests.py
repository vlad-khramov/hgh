from django.test import TestCase
from apps.main.models import Hero, Unit


class SimpleTest(TestCase):

    def setUp(self):
        self.hero = Hero(
            attack_github = 2,
            attack_own = 3
        )

    def test_hero_stats(self):
        """
        tests correct getting stats of hero
        """
        assert self.hero.get_attack() == 5


    def test_unit_stats(self):
        """
        tests correct getting stats of hero
        """
        unit = Unit(
            hero = self.hero,
            attack_github = 4
        )

        assert unit.get_attack() == 9


