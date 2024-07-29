from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib import messages

from confectionery.models import Product
from .cart import Cart
from .forms import AddToCartProductForm


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


# @require_POST # این دکوریتور باعث میشه که فقط با متد پست بشه این تابع رو صدا کرد
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])
    return redirect('cart:cart_detail')


# @require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


# @require_POST
def clear_cart(request):
    cart = Cart(request)
    if len(cart):
        cart.clear()
        messages.success(request, _('All products successfully removed from your cart'))
    else:
        messages.warning(request, _('Your cart is already empty.'))
    return redirect('product_list')
