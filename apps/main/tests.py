from django.contrib.auth.models import User
from django.test import TestCase
from apps.main.models import Hero, Unit


class SimpleTest(TestCase):


    def setUp(self):
        self.user, created = User.objects.get_or_create(username='fakeuser', email='fake@pukkared.com', password='mypassword', first_name='fakename')

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
        hero = Hero(user=self.user)
        hero.save()
        Unit(hero=hero,race='human').save()
        Unit(hero=hero,race='elf').save()
        Unit(hero=hero,race='elf').save()

        hero.update_race()


        assert hero.race == 'elf'


