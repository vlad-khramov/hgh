from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def hero_main_info(context, hero):
    return """
        <h2>%s [%s]</h2>
        %s<br>
        %s<br><br>

        Wins: %s<br>
        Defeats: %s<br><br>

        Attack: %s<br>
        Defence: %s<br>
        Attentiveness: %s<br>
        Charm: %s<br>
    """ % (
        hero.login,
        hero.level,
        hero.name,
        hero.race,
        hero.wins,
        hero.losses,
        hero.get_attack(),
        hero.get_defence(),
        hero.get_attentiveness(),
        hero.get_charm(),
        )
