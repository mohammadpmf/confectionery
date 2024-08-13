import requests
import json, random, string

from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _

from .signals import order_paid

from orders.models import Order
from cart.madval_functions import clear_user_cart_in_db, load_cart_from_db_to_session
from cart.cart import Cart


############################################ Sandbox ############################################
def payment_process_sandbox(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10 # موقع تست دیدم خودش تومان هست دیگه من ریال رو استفاده نکردم
    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
    request_data = {
        'MerchantID': settings.ZARINPAL_MERCHANT_ID,
        'Amount': toman_total_price,
        'Description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'CallbackURL': request.get_host() + reverse('payment:payment_callback_sandbox')
    }
    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    data = response.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()
    if ('errors' not in data) or (len(response.json()['errors']) == 0):
        return payment_callback_sandbox(request)
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/%s' %authority) # سایتش ارور میداد فعلا بیخیال شد.
    else:
        messages.error(request, _("Error from Zarinpal"))
        return redirect('homepage')


def payment_callback_sandbox(request):
    cart = Cart(request) # برای این که اگه موفقیت آمیز نبود دوباره کارت رو پر کنیم.
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')
    # order = get_object_or_404(Order, zarinpal_authority=payment_authority) 
    # چون زرین پال جواب نمیداد و نداشتم اون عدد رو، گفتم بره از دیتابیس خودم بخونه. اگه
    # اون درست شد. به جای این دو خط بعدی که اردر رو این طوری گرفتم میتونم با اون یه خطی که
    # کامنت کردم بگیرمش.
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    # if payment_status=='OK':
    # زرین پال که جواب داد این رو درست کنم. الان چون جواب نمیده اوکی نیست و خودم برای این
    # که کار کنه ایف ترو گذاشتم. اگه درست شد این ایف رو حذف کنم و قبلی رو بذارم.
    if True:
        request_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        request_data = {
            'MerchantID': settings.ZARINPAL_MERCHANT_ID,
            'Amount': rial_total_price,
            'Authority': payment_authority, # ۳۶ تا کاراکتر باید باشه که چون هیچی نبود وارد ایف اول نمیشد. الکی یه چیز دادم که بشه و ارور بعدی رو بده. این خط بعدی رو بعدا پاک کنم.
            'Authority': "132132132132131132131131324234234232",
        }
        response = requests.post(
            url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
            data=json.dumps(request_data),
            headers=request_header,
        )
        if 'errors' not in response.json():
            data = response.json()
            payment_code = data['Status']
            payment_code=-33 # برای این که همیشه موفق باشه
            if payment_code==-33:
                order.is_paid=True
                order.zarinpal_ref_id = data['RefID']
                order.zarinpal_data = data
                madval_tracking_code = ''.join(random.choices(string.ascii_uppercase+string.digits, k=8))
                order.madval_tracking_code = madval_tracking_code
                order.save()
                if request.user.is_authenticated: # حتما لاگین هست که تا اینجا رسیده. ولی گفتم روزه شک دار نگیرم.
                    clear_user_cart_in_db(request.user)
                email = request.user.email if request.user else None
                order_paid.send_robust("payment_callback_sandbox", order=order, email=email)
                return render(request, 'result_success.html', {'tracking_code': madval_tracking_code})
            elif payment_code==101:
                load_cart_from_db_to_session(request.user, cart)
                error = _('This transaction has been registered once!')
                return render(request, 'result_error.html', {'error': error})
            else:
                load_cart_from_db_to_session(request.user, cart)
                error = _("Transaction failed!")
                return render(request, 'result_error.html', {'error': error})
        else:
            load_cart_from_db_to_session(request.user, cart)
            error = response.json().get('errors')
            return render(request, 'result_error.html', {'error': error})
    else:
        load_cart_from_db_to_session(request.user, cart)
        error = _("Transaction failed!")
        return render(request, 'result_error.html', {'error': error})












############################################ Real ############################################
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10 # موقت تست دیدم خودش تومان هست دیگه من ریال رو استفاده نکردم
    # از اینجا به بعد فقط باهاش نوشتم که نمونه داشته باشم. مال ۲ سال پیش بود.
    # احتمال زیاد یو آر ال زرین پال عوض شده و کار نکنه. از طرفی باید کد من هم تایید میشد که
    # نماد اعتماد نگرفتم و تایید نشد و کار نمیکنه. اما با همین وضع دارم کامیت میکنم.
    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': toman_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': request.get_host() + reverse('payment:payment_callback')
    }
    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    data = response.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if ('errors' not in data) or (len(response.json()['errors']) == 0):
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse("Error from Zarinpal")


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')
    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status=='OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': payment_authority,
        }
        response = requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header,
        )
        if 'data' in response.json() and ('errors' not in response.json()['data']) or (len(response.json()['data']['errors']) == 0):
            data = response.json()['data']
            payment_code = data['code']
            if payment_code==100:
                order.is_paid=True
                order.ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()
                return HttpResponse('پرداخت موفق')
            elif payment_code==101:
                return HttpResponse('این تراکنش قبلا ثبت شده است.')
            else:
                error_code = response.json()['errors']['code']
                error_message = response.json()['errors']['message']
                return HttpResponse(f'{error_code} {error_message} تراکنش ناموفق')
    else:
        return HttpResponse('تراکنش ناموفق')

























########################### az_iranian_bank_gateways ###########################
# نصبش کردم. اما درست کار نمیکرد کامنت کردم. کدهاش رو حذف نکردم.
# import logging
# from django.urls import reverse
# from django.shortcuts import render
# from django.http import HttpResponse, Http404

# from azbankgateways.exceptions import AZBankGatewaysException
# from azbankgateways import (
#     bankfactories,
#     models as bank_models,
#     default_settings as settings,
# )


# def go_to_gateway_view(request):
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#     toman_total_price = order.get_total_price()
#     user_mobile_number = order.phone_number
#     factory = bankfactories.BankFactory()
#     try:
#         bank = (
#             factory.auto_create()
#         )  # or factory.create(bank_models.BankType.BMI) or set identifier
#         bank.set_request(request)
#         bank.set_amount(toman_total_price)
#         bank.set_client_callback_url(reverse("payment:payment_callback_sandbox"))
#         bank.set_mobile_number(user_mobile_number)  # اختیاری
#         bank_record = bank.ready()
#         context = bank.get_gateway()
#         return render(request, "redirect_to_bank.html", context=context)
#     except AZBankGatewaysException as e:
#         logging.critical(e)
#         return render(request, "redirect_to_bank.html", {'errors': e})



# def callback_gateway_view(request):
#     tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
#     if not tracking_code:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404

#     try:
#         bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
#     except bank_models.Bank.DoesNotExist:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404

#     # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
#     if bank_record.is_success:
#         # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
#         # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
#         return HttpResponse("پرداخت با موفقیت انجام شد.")

#     # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
#     return HttpResponse(
#         "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
#     )