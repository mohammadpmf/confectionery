from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.validators import MaxLengthValidator, MinLengthValidator


class Order(models.Model):
    user = models.ForeignKey(verbose_name=_('User'), to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
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
