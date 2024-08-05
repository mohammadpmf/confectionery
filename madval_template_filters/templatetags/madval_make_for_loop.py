from django import template

register = template.Library()


@register.filter(name='times') 
def times(number):
    if number==None:
        number=0
    return range(number)


@register.filter
def get_n_first_objects(query, n=5):
    return query[:n]


@register.filter
def get_n_last_objects(query, n=5):
    length = len(query)
    if length>n:
        return query[length-n:]
    return query
