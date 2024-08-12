from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db import transaction

from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem


@login_required
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart)==0:
        messages.warning(request, _('You can not proceed to checkout because your cart is empty.'))
        return redirect('homepage')
    
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            with transaction.atomic():
                order_obj = order_form.save(commit=False)
                order_obj.user = request.user
                order_obj.save()
                for item in cart:
                    product = item['product_obj']
                    OrderItem.objects.create(
                        order=order_obj,
                        product=product,
                        quantity=item['quantity'],
                        price=product.price_toman
                    )
                cart.clear()
                temp = request.POST.get('change_name')
                if temp: # اگه تیک زده باشه استرینگ on و اگه نزده باشه None رو میفرسته که استرینگ نیست. نان تایپ هست.
                    request.user.first_name = request.POST.get('first_name')
                    request.user.last_name = request.POST.get('last_name')
                    request.user.save()
                request.session['order_id'] = order_obj.id
                return redirect('homepage')
                return redirect('payment:payment_process')
        else:
            context={
                'form': order_form
            }
            return render(request, 'orders/order_create.html', context)

    context={
        'form': order_form
    }
    return render(request, 'orders/order_create.html', context)