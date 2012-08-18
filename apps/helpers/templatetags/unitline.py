from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def unitline(context, unit):
    return """
        <b>%s</b>, %s (%s/%s/%s/%s) <a href="http://github.com/%s/%s">[g]</a>
    """ % (
        unit.custom_name,
        unit.race,
        unit.get_attack(),
        unit.get_defence(),
        unit.get_attentiveness(),
        unit.get_charm(),
        unit.hero.login,
        unit.name
        )
