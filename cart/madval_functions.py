from .models import UserCart, CartItem

from confectionery.models import Product


# def save_cart_in_db(user, cart: dict):
#     db_cart = UserCart.objects.prefetch_related('items').filter(user=user).first()
#     if not db_cart: # اگه از قبل نبود میسازیم. اگر هم بود که تو خط قبل گرفتیمش.
#         db_cart = UserCart.objects.create(user=user)
#     clear_user_cart_in_db(user)
#     for product_id_str, quantity_dict in cart.items():
#         product_id = int(product_id_str)
#         quantity=quantity_dict.get('quantity')
#         CartItem.objects.create(cart=db_cart, product_id=product_id, quantity=quantity)
       

def save_cart_in_db(user, cart: dict):
    db_cart = UserCart.objects.prefetch_related('items').filter(user=user).first()
    if not db_cart: # اگه از قبل نبود میسازیم. اگر هم بود که تو خط قبل گرفتیمش.
        db_cart = UserCart.objects.create(user=user)
    for product_id_str, quantity_dict in cart.items():
        product_id = int(product_id_str)
        quantity = quantity_dict.get('quantity')
        cart_item = CartItem.objects.filter(cart=db_cart, product_id=product_id).first()
        if not cart_item:
            CartItem.objects.create(cart=db_cart, product_id=product_id, quantity=quantity)
        else:
            cart_item.quantity=quantity
            cart_item.save()


def remove_cart_item_from_db(user, product_id):
    db_cart = UserCart.objects.filter(user=user).first()
    if db_cart: # اگه وجود نداشت پس لازم نیست کاری بکنیم. اگه داشت این آیتم رو حذف میکنیم.
        CartItem.objects.filter(cart=db_cart, product_id=product_id).delete()


def clear_user_cart_in_db(user):
    db_cart = UserCart.objects.filter(user=user).first()
    if db_cart: # اگه چیزی بود که پاک میکنیم. اگه نبود هم که لازم نیست کاری کنیم.
        CartItem.objects.filter(cart=db_cart).delete()
    # خود کارت رو دیگه حذف نکردم. چون هم یه دستور اضافه هست و هم بعدا دوباره یه کارت
    # با آی دی جدید برای این یوزر باید بسازیم. چه کاریه. کارت خودش رو داره هر بار که اومد
    # خرید از همون استفاده میکنه دیگه 😁 تازه میتونیم بفهمیم که اولین خریدش هم چه زمانی بوده.


def load_cart_from_db_to_session(user, session_cart):
    message = None # برای این که اگه تعداد آیتم ها بیشتر از ۳۰ تا شد پیغام بدم.
    db_cart = UserCart.objects.prefetch_related('items__product').filter(user=user).first()
    session_items = {} # آیتم هایی که قبل از لاگین به سبد خرید اضافه کرده رو داخل این ذخیره میکنیم.
    # یه دیکشنری که کلیدش آی دی ها هست و مقدارش تعدادی که از اون آیتم اضافه کرده.
    for product_id_str, quantity_dict in session_cart.cart.items():
        product_id = int(product_id_str)
        quantity = quantity_dict.get('quantity')
        session_items[product_id] = quantity
    if db_cart: # اگه سبد خریدش وجود داشت که یک سری کارها رو میکنیم. اگه نبود که خب خالیه.
        for cart_item in db_cart.items.all():
            cart_item: CartItem
            final_quantity = cart_item.quantity + session_items.get(cart_item.product.id, 0)
            if final_quantity>30:
                message = ">30"
                final_quantity=30
            session_cart.add(product=cart_item.product, quantity=final_quantity, replace_current_quantity=True, give_message=False)
            # اول این شکلی نوشته بودم. بعد دیدم با تابع گت دیکشنری چقدر باحال تر و خفن تر
            # میشه نوشت و مدل خط های بالا نوشتم. اما گذاشتم اینا هم باشه. چون بعدا که ببینم
            # احتمالا یادم نیاد چرا این شکلی نوشتم.
            # if cart_item.product.id in session_items.keys(): # یعنی از قبل چند تا تو دیتابیس بوده.
            #     # چند تا هم الان اضافه کرده. منتهی باید چک کنم که از ۳۰ تا بیشتر نشه.
            #     if cart_item.quantity + session_items.get(cart_item.product.id)>30:
            #         session_cart.add(product=cart_item.product, quantity=30, replace_current_quantity=True, give_message=False)
            #     else:
            #         session_cart.add(product=cart_item.product, quantity=cart_item.quantity, replace_current_quantity=False, give_message=False) # چون باید اضافه کنه.
            # else: # یعنی از قبل تو دیتابیس نبوده. پس باید الان اضافه اش کنه
            #     session_cart.add(product=cart_item.product, quantity=cart_item.quantity, replace_current_quantity=True, give_message=False)
    return message
