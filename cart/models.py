from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from confectionery.models import Product


class UserCart(models.Model):
    user = models.OneToOneField(verbose_name=_('User'), to=get_user_model(), on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(verbose_name=_('User'), auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(verbose_name=_('Cart'), to=UserCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(verbose_name=_('Product'), to=Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(verbose_name=_('Quantity'))

    class Meta:
        unique_together = [['cart', 'product']]
