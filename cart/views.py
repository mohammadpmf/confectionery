from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib import messages

from .cart import Cart
from .forms import AddToCartProductForm
from .madval_functions import clear_user_cart_in_db, remove_cart_item_from_db, save_cart_in_db

from confectionery.models import Product


def cart_detail_view(request):
    cart = Cart(request)
    for item in cart:
        item['product_update_quantity_form'] = AddToCartProductForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })
    return render(request, 'cart/cart_detail.html', {'cart': cart})
    # البته بعد از این که تبدلیش کردیم به یه کانتکست پراسسور لازم نیست دیگه اینجا بفرستیمش برای
    # تمپلیت. چون اونجا قابل دسترسی هست خودش. اما گذاشتم باشه شاید تو یه پروژه ای تبدیلش نکردیم
    # و فقط خواستیم تو صفحه جزییات ببینیمش.


@require_POST # این دکوریتور باعث میشه که فقط با متد پست بشه این تابع رو صدا کرد
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)
    next_page:str = request.POST.get('next_page')
    if not next_page:
        next_page = 'cart:cart_detail'
    elif next_page.startswith('category-product'):
        next_page = reverse('categories', args=[product.product_type]) + "#" + next_page
    elif next_page.startswith('product'):
        # next_page = reverse('product_detail', args=[product_id]) + "#" + next_page
        # برای این گذاشتم جالب نشد. چون خودش بالای صفحه بود یه خورده میومد پایین الکی. اما
        # پاک نکردم آی دی اچ تی ام الش ر. فقط اینجا ازش استفاده نکردم.
        next_page = reverse('product_detail', args=[product_id])
    elif next_page.startswith('favorites'):
        next_page = reverse('my_favorites') + "#" + next_page
    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data.get('quantity')
        cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])
        if user.is_authenticated: # اگه یوزر داخل نبود که مهم نیست و کاری نمیکنیم. ولی اگه بود تو دیتابیس هم ذخیره میکنیم اطلاعات فعلی کارت رو
            save_cart_in_db(user, cart.cart)
    else:
        messages.error(request, form.errors)
    return redirect(next_page)


@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if user.is_authenticated: # اگه یوزر داخل نبود که مهم نیست و کاری نمیکنیم. ولی اگه بود تو دیتابیس هم ذخیره میکنیم اطلاعات فعلی کارت رو
        remove_cart_item_from_db(user, product_id)
    return redirect('cart:cart_detail')


@require_POST
def clear_cart(request):
    cart = Cart(request)
    user = request.user
    if len(cart):
        cart.clear()
        if user.is_authenticated:
            clear_user_cart_in_db(user)
        messages.success(request, _('All products successfully removed from your cart'))
    else:
        messages.warning(request, _('Your cart is already empty.'))
    return redirect('homepage')
