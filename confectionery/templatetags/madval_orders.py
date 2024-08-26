from django import template

from orders.models import Order

register = template.Library()


@register.filter
def how_many_times_used_by_this_user(discount, user):
    return Order.objects.filter(user=user, discount=discount).count()


@register.filter
def how_many_times_used(discount):
    return Order.objects.filter(discount=discount).count()
