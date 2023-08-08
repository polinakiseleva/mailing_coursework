from django import template

register = template.Library()


@register.filter()
def mymedia(value):
    if value:
        return f'/media/{value}'

    return '#'


@register.simple_tag()
def my_path(value):
    if value:
        return f"/media/{value}"
    return "#"
