from django.template import Library


register = Library()

@register.simple_tag
def page_link(page_number, params, anchor):
    link = '?page=%s' % page_number
    if params:
        link = '%s&amp;%s' % (link, params.replace('&', '&amp;'))
    if anchor:
        link += '#%s' % anchor
    return link
