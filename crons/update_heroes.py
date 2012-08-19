"""
Script for updating heroes and their armies by cron
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'hgh.local_settings'
from apps.helpers.gh import get_user
from apps.main.models import Hero

for hero in Hero.objects.filter().order_by('last_update'):
    user_info = get_user(hero.login)
    if not user_info:
        continue

    hero.update_from_response(user_info)
    hero.update_army()
    hero.save()