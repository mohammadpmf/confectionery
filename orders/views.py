from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db import transaction

from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem, Order, Discount


@login_required
def order_create_view(request):
    cart = Cart(request)
    if len(cart)==0:
        messages.warning(request, _('You can not proceed to checkout because your cart is empty.'))
        return redirect('homepage')
    if request.method=='GET':
        last_order = Order.objects.filter(user=request.user).order_by('datetime_created').last()
        if last_order: # اگه قبلا سفارشی ثبت کرده بود، اسم، فامیل، شماره و آدرسش رو از آخرین
            # سفارشش میاریم که فرمش پر شده باشه کارش راحت تر باشه
            initial_date = {
                'first_name': last_order.first_name,
                'last_name': last_order.last_name,
                'address': last_order.address,
                'phone_number': last_order.phone_number,
            }
        else:
            initial_date={}
        order_form = OrderForm(instance=request.user, initial=initial_date)

        sent_discount_text = request.GET.get('discount_text')
        discount_amount=0
        if sent_discount_text: # اگه طرف چیزی ارسال کرده بود بررسی میکنیم. اما دفعه اول که میخواد صفحه رو نشون بده که قاعدتا نباید بهش ارور بدیم. چون کدی وارد نکرده.
            discount = Discount.objects.prefetch_related('orders__user').filter(text=sent_discount_text).first()
            if not discount:
                messages.error(request, _('This discount code is not verified!'))
            else:
                if discount.is_expired:
                    messages.error(request, _('Sorry. This discount code is expired!'))
                elif discount.user and discount.user!=request.user: # اگه برای یوزر خاصی بود و با اون یوزر درخواست نداده
                    messages.error(request, _('Sorry. This discount code is not for your account!'))
                else:
                    used_times_counter_for_this_user = 0
                    for tmp_order in discount.orders.all():
                        if tmp_order.user==request.user:
                            used_times_counter_for_this_user+=1
                    if used_times_counter_for_this_user>=discount.same_user_limit:
                        messages.error(request, _('Sorry. The maximum use of this discount code '
                                'has reached for your account!'))
                    else:
                        discount_amount = discount.discount_amount
                        if not discount_amount:
                            discount_amount = round(cart.get_total_price()*discount.discount_percentage)
                            # اینجا صدا کردن کارت دات گت توتال پرایس باعث میشه یه کوئری مشابه بزنه. اما
                            # گفتم ارزش وسواس خرج دادن نداره. دیگه همین طوری نوشتمش.
                            max_amount = discount.max_discount_amount
                            if discount_amount>max_amount:
                                discount_amount=max_amount
                        if cart.get_total_price()-discount_amount<10000:
                            messages.error(request, _('Sorry, the price after '
                                "discount is less than 10000 Toman. We cant't "
                                'checkout that order. Please choose another '
                                'item that make total price more than 10000 Toman.'))
                            discount_amount = 0
                        else:
                            messages.success(request, _('Discount successfully applied to your order.'))
        context = {
            'form': order_form,
            'discount_text': sent_discount_text,
            'discount_amount': discount_amount,
        }
        return render(request, 'orders/order_create.html', context)
    elif request.method == 'POST':
        sent_discount_text = request.POST.get('discount_text')
        discount_amount=0
        discount_status = 0 # تو حالت هپی پث باید مثل همون گت باشه و بدون مشکل کار کنه.اما ممکنه
        # یکی بخواد کرم بریزه و اچ تی ام ال رو دستکاری کنه. پس اینجا هم چک میکنم که مشکلی پیش نیاد.
        # 0  => بدون کد تخفیف
        # 1  => دارای کد تخفیف
        # -1 => مشکل دار
        if sent_discount_text:
            discount = Discount.objects.prefetch_related('orders__user').filter(text=sent_discount_text).first()
            if not discount:
                messages.error(request, _('This discount code is not verified!'))
                discount_status = -1
            else:
                if discount.is_expired:
                    messages.error(request, _('Sorry. This discount code is expired!'))
                    discount_status = -1
                elif discount.user and discount.user!=request.user: # اگه برای یوزر خاصی بود و با اون یوزر درخواست نداده
                    messages.error(request, _('Sorry. This discount code is not for your account!'))
                    discount_status = -1
                else:
                    used_times_counter_for_this_user = 0
                    for tmp_order in discount.orders.all():
                        if tmp_order.user==request.user:
                            used_times_counter_for_this_user+=1
                    if used_times_counter_for_this_user>=discount.same_user_limit:
                        messages.error(request, _('Sorry. The maximum use of this discount code '
                                'has reached for your account!'))
                        discount_status = -1
                    else:
                        discount_amount = discount.discount_amount
                        if not discount_amount:
                            discount_amount = round(cart.get_total_price()*discount.discount_percentage)
                            max_amount = discount.max_discount_amount
                            if discount_amount>max_amount:
                                discount_amount=max_amount
                        if cart.get_total_price()-discount_amount<10000:
                            messages.error(request, _('Sorry, the price after '
                                "discount is less than 10000 Toman. We cant't "
                                'checkout that order. Please choose another '
                                'item that make total price more than 10000 Toman.'))
                            discount_amount = 0
                            discount_status = -1
                        else:
                            # messages.success(request, _('Discount successfully applied to your order.'))
                            # اینجا دیگه پیغام ندادم.
                            discount_status = 1
        order_form = OrderForm(request.POST)
        if discount_status in[0, 1] and order_form.is_valid():
            with transaction.atomic():
                order_obj = order_form.save(commit=False)
                order_obj.user = request.user
                if discount_status==1:
                    order_obj.discount=discount # اینجا فقط برای خود اردر تخفیف رو ثبت میکنیم.
                    # به دیسکَونت کاری نداریم. بعد از پرداخت درگاه بانکی، یکی به تعداد استفاده شده های
                    # دیسکَونت اضافه میکنیم. اگه الان اضافه کنیم شاید طرف کنسل کنه هدر بره. بعد از
                    # پرداخت موفق اضافه میکنم. اما تو این اردر تخفیف ثبت میشه. اگه مشکلی پیش اومد
                    # بعدا دستی درستش میکنیم. مثل تخفیف من تو انسپ
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
                return redirect('payment:payment_process_sandbox')
        else:
            context = {
                'form': order_form,
                'discount_text': sent_discount_text,
                'discount_amount': discount_amount,
            }
            return render(request, 'orders/order_create.html', context)
