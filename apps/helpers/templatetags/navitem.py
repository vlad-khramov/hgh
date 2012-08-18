from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def navitem(context, url, name):
    return """
    <li%s>
        <a href="%s">%s</a>
    </li>
    """ % (
        ' class="active"' if context['request'].path == reverse(url) else '',
        reverse(url),
        name
        )
