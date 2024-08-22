from django import template

register = template.Library()


@register.filter(name='sub')
def sub(first, second):
    return first-second