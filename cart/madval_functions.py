from .models import UserCart, CartItem

from confectionery.models import Product


# این ورژن اولی بود که برای ذخیره داخل کارت نوشتم. برای اضافه کردن و تغییر دادن درست
# کار میکرد. اما موقع پاک کردن درست نبود. موقع پاک کردن هم همین تابع رو صدا کردم.
# اما باید کد رو اصلاح میکردم. این شکلی که آیتم هایی که هستند رو ویرایش کنه.
# میشد نوشت اما عجله ای بود. راه حل ساده تر رو انتخاب کردم. گفتم کلا هر بار که یه
# چیزی رو اضافه میکنیم یا پاک میکنیم، موقع سیو کردن، بیاد کلا سبد خرید رو خالی کنه
# و از اول آیتم های سشن رو اضافه کنه و به شدت تعداد آی دی ها بالا میره.
# یعنی من ۵ تا محصول که اضافه میکنم دونه دونه، آی دی آخر به جای این که ۵ باشه
# میشه ۱۵. اولی رو که اضافه کردم هیچی. دومی رو که اضافه میکنم همه رو پاک میکنه دوباره
# اولی و دومی رو میذاره. و آی دی ها هر بار از ادامه اش به تعداد آیتم ها اضافه میشه.
# تا به میلیارد برسه خیلیه و به خاطر همین همین شکلی سریع درستش کردم. اما از نظر حافظه
# هم به نظرم خوب نیست و در ۲۰ سال موجب خرابی زودتر هارد یا اس اس دی میشه. سر فرصت بعدا
# درستش کنم. اما فعلا روش ساده تر رو انجام دادم که هم سریعتر بود و هم کد کمتری نوشتم.
# def save_cart_in_db(user, cart: dict):
#     db_cart = UserCart.objects.prefetch_related('items').filter(user=user).first()
#     if not db_cart: # اگه از قبل نبود میسازیم. اگر هم بود که تو خط قبل گرفتیمش.
#         db_cart = UserCart.objects.create(user=user)
#     for product_id_str, quantity_dict in cart.items():
#         product_id = int(product_id_str)
#         quantity=quantity_dict.get('quantity')
#         cart_item = CartItem.objects.filter(cart=db_cart, product_id=product_id).first()
#         if not cart_item:
#             CartItem.objects.create(cart=db_cart, product_id=product_id, quantity=quantity)
#         else:
#             cart_item.quantity=quantity
#             cart_item.save()


def save_cart_in_db(user, cart: dict):
    db_cart = UserCart.objects.prefetch_related('items').filter(user=user).first()
    if not db_cart: # اگه از قبل نبود میسازیم. اگر هم بود که تو خط قبل گرفتیمش.
        db_cart = UserCart.objects.create(user=user)
    clear_user_cart_in_db(user)
    for product_id_str, quantity_dict in cart.items():
        product_id = int(product_id_str)
        quantity=quantity_dict.get('quantity')
        CartItem.objects.create(cart=db_cart, product_id=product_id, quantity=quantity)
       

def clear_user_cart_in_db(user):
    db_cart = UserCart.objects.prefetch_related('items').filter(user=user).first()
    if db_cart: # اگه چیزی بود که پاک میکنیم. اگه نبود هم که لازم نیست کاری کنیم.
        for item in db_cart.items.all():
            item.delete()
    # خود کارت رو دیگه حذف نکردم. چون هم یه دستور اضافه هست و هم بعدا دوباره یه کارت
    # با آی دی جدید برای این یوزر باید بسازیم. چه کاریه. کارت خودش رو داره دیگه. 😁


def load_cart_from_db_to_session(user, cart):
    db_cart = UserCart.objects.prefetch_related('items__product').filter(user=user).first()
    if db_cart: # اگه سبد خریدش وجود داشت که یک سری کارها رو میکنیم. اگه نبود که خب خالیه.
        for cart_item in db_cart.items.all():
            cart.add(product=cart_item.product, quantity=cart_item.quantity, replace_current_quantity=True, give_message=False)
