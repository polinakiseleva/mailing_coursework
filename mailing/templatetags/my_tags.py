from django import template

register = template.Library()


@register.simple_tag()
def my_path(object):
    if object:
        return f"/media/{object}"
    return "#"


@register.filter()
def my_path(object):
    if object:
        return f"/media/{object}"
    return "#"
