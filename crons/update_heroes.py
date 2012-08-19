# coding: utf-8
"""
Script for updating heroes and their armies by cron
"""
import os
import sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'hgh.local_settings'
from apps.helpers.gh import get_user
from apps.main.models import Hero
from apps.helpers.gh import get_events

IGNORED_EVENTS = (
    'WatchEvent', 'FollowEvent', 'ForkEvent', 'MemberEvent', 'GollumEvent',
    'CommitCommentEvent', 'DeleteEvent', 'PublicEvent', 'ForkApplyEvent',
    'TeamAddEvent'
)
EVENT_TO_SPELL = {
    'PushEvent': 'UnitBuf', 
    'IssueCommentEvent': 'HeroBuf', 
    'IssuesEvent': 'Lightning',
    'PullRequestEvent': 'Fireball', 
    'CreateEvent': 'ChainLightning',
    'PullRequestReviewCommentEvent': 'TitanSkin',
    'GistEvent': 'Amnezia',
    'DownloadEvent': 'ThornsAura',
}

def produce_spells(hero, event_list):
    for event_dict in event_list:
        ev_type = event_dict['type']
        Event.objects.create(
            user=hero.user, type=ev_type, date=event_dict['created_at']
        )
        obj, created = Spell.objects.get_or_create(
            hero=hero, 
            type=EVENT_TO_SPELL.get(ev_type, 'UnknownSpell')
        )
        if not created:
            obj.cnt += 1
            obj.save()
        
for hero in Hero.objects.filter().order_by('last_update')[:1000]:
    user_info = get_user(hero.login)
    if not user_info:
        continue

    hero.update_from_response(user_info)
    hero.update_army()
    hero.save()
    try:
        newest_date = Event.objects.filter(user=hero.user).order_by('-date')[0]
    except IndexError:
        newest_date = datetime.datetime(2000, 01, 01)
    produce_spells(hero, [
        evt for evt in get_events()
        if evt['created_at']>=newest_date and evt['type'] not in IGNORED_EVENTS
    ])