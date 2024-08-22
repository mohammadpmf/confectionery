from datetime import date
from random import choices, randint
from string import ascii_uppercase, digits

from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError


def generate_random_code():
    return ''.join(choices(ascii_uppercase+digits, k=randint(8, 10)))


class Discount(models.Model):
    text = models.CharField(verbose_name=_('Text'), max_length=31, unique=True, default=generate_random_code)
    discount_amount = models.PositiveIntegerField(verbose_name=_('Discount Amount'), blank=True, null=True)
    discount_percentage = models.DecimalField(verbose_name=_('Discount Percentage'), max_digits=2, decimal_places=2, blank=True, null=True)
    max_discount_amount = models.PositiveIntegerField(verbose_name=_('Max Discount Amount'), default=150000)
    limit = models.PositiveIntegerField(default=10)
    used_times = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField()
    user = models.ForeignKey(verbose_name=_('User'), to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='discounts', blank=True, null=True)

    def clean(self):
        super().clean()
        if self.discount_amount in [None, ''] and self.discount_percentage in [None, '']:
            raise ValidationError(_("You should choose either discount_amount or discount_percentage!\nBoth of them can't be Null!"))
        elif self.discount_amount not in [None, ''] and self.discount_percentage not in [None, '']:
            raise ValidationError(_("You should choose one of discount_amount or discount_percentage!\nYou can't choose both of them at the same time!"))

    @property
    def is_expired(self):
        if date.today()>self.expiration_date:
            return True
        return self.used_times>=self.limit


class Order(models.Model):
    user = models.ForeignKey(verbose_name=_('User'), to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    discount = models.ForeignKey(verbose_name=_('Discount'), to=Discount, on_delete=models.PROTECT, related_name='orders', blank=True, null=True)
    is_paid = models.BooleanField(verbose_name=_('Is Paid?'), default=False)

    first_name = models.CharField(verbose_name=_('First Name'), max_length=255)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=255)
    phone_number = models.CharField(verbose_name=_('Phone Number'), max_length=14, validators=[
        MinLengthValidator(11, _("Phone number should be at least 11 digits")),
        MaxLengthValidator(14, _("Phone number should be at most 14 digits"))
        ],
    )
    address = models.TextField(verbose_name=_('Address'), max_length=500)
    
    order_notes = models.TextField(verbose_name=_('Order Notes'), max_length=1000, blank=True)

    zarinpal_authority = models.CharField(max_length=255, blank=True) # این رو برای ذخیره کد پیگیری زرین پال تعریف کردیم.
    zarinpal_ref_id = models.CharField(max_length=255, blank=True) # این رو برای ذخیره کد پیگیری زرین پال تعریف کردیم.
    zarinpal_data = models.TextField(blank=True)
    madval_tracking_code = models.CharField(max_length=255, default=0)
    
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Time of creation'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date Time of last edit'))

    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_price(self):
        # total_price = 0
        # for item in self.items.all():
        #     item: OrderItem
        #     total_price += item.price*item.quantity
        # return total_price
        return sum(item.price*item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(verbose_name=_('Order'), to=Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(verbose_name=_('Product'), to='confectionery.Product', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'), default=1)
    price = models.PositiveIntegerField(verbose_name=_('Price'))

    def __str__(self):
        return f"OrderItem {self.id}: {self.product} x {self.quantity} Price: {self.price}"
