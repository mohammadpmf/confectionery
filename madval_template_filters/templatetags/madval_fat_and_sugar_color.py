from django import template

register = template.Library()


@register.filter(name='get_color')
def get_color(value):
    value = str(value)
    if value=='high':
        return 'red'
    if value=='avg':
        return 'orange'
    if value=='low':
        return 'green'
