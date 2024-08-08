from django.contrib import messages
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from cart.cart import Cart
from cart.madval_functions import load_cart_from_db_to_session


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if user.is_authenticated:
        cart = Cart(request)
        message = load_cart_from_db_to_session(user, cart)
        if message==">30":
            messages.warning(request, _("The number of items can not be more than 30. So the cart items which had more than 30 items changed to 30."))
            # اول مسیج رو اون ور درست کردم و اینجا متغیر مسیج رو گذاشتم. اما وقتی دستور
            # میک مسجز رو میزدم نمیساخت. این بود که این شکلی نوشتم این ایف رو.

# وقتی این رو درست کردم، فهمیدم که بهتر بود برای ذخیره سبد خرید قبل از خروج توی دیتابیس
# هم از سیگنال استفاده کنم. اما دیگه انجام نمیدم فعلا.