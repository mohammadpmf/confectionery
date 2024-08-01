from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, login
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password

from requests.exceptions import ConnectTimeout
import ghasedakpack
import random

from config.madval1369_secret import *
from .models import PhoneNumber
from . import forms



class LoginWithPhoneNumber(generic.TemplateView):
    template_name = 'login_with_phone_number.html'

    otps = dict() # توی تابع اینیت که مینوشتم درست کار نمیکرد. اما اینجا به عنوان کلاس اتربیوت در نظر
    # گرفتم جواب داد. با این حال رو استرینگ کار نمیکرد. اما روی دیکشنری و لیست و مجموعه که به یه
    # جای حافظه اشاره میکنن با سلف دسترسی داشتم و میتونستم تو متد گت مقدار رمز رو ذخیره کنم و تو
    # متد پست ببینم یکی هست یا نه. اما برای استرینگ نمیشد. برای استرینگ هم به جای این که با سلف
    # صداش کنم با اسم کلاس صداش کردم درست شد. به خاطر همین برای همین متغیر او تی پیز که قراره رمزهای
    # یکبار مصرف رو نگه داره، با این که سلف اینجا کار رو دیکشنری جواب داد، با اسم کلاس صداش کردم.
    # باز هم میگم تو اینیت نوشتم جواب نمیداد. یعنی بعد از این که متد گت صدا میشد و تغییرش میدادم،
    # وقتی میرفتم تو متد پست اون مقدار نبود و یه دیکشنری خالی بود دوباره.

    def __init__(self, **kwargs):
        self.sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)
        self.good_line_number_for_sending_otp = '30005088' # مال خودم رو که میذارم، شانسی از این شماره یا 20008580 میفرسته که شماره ۳۰۰۰ اوکی هست. ولی ۲۰۰۰ داغانه یه بار تقریبا ۲۰ دقیقه طول کشید تا بفرسته که خب دیگه یکبار رمز به درد بخوری نیست.

        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get('phone_number')
        otp = str(random.randint(100000, 999999))
        messages.warning(request, f"otp is {otp}😊")
        LoginWithPhoneNumber.otps[phone_number]=otp
        try:
            username = PhoneNumber.objects.select_related('user').get(phone_number=phone_number)
        except PhoneNumber.DoesNotExist:
            username = None
        context = {
            'username': username,
            'phone_number': phone_number,
        }
        try:
            # answer = self.sms.verification({'receptor': phone_number, 'linenumber': self.good_line_number_for_sending_otp,'type': '1', 'template': MY_TEMPLATE_NAME_IN_GHASEDAK_ME_SITE, 'param1': otp})
            answer = True
            if answer:
                messages.success(request, _("A verification code sent to %s. Please enter the recieved code to continue." %phone_number))
                return render(request, 'login_with_phone_number.html', context)
            messages.error(request, _("A problem occured in sending message. Please try again in a few minutes."))
            return redirect('account_login')
        except ConnectTimeout as error:
            messages.error(request, _("A problem occured in sms message server. Please try again in a few minutes."))
            messages.error(request, _(error))
            return redirect('account_login')
    
    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('user_name')
        sent_otp = request.POST.get('otp')
        otps = LoginWithPhoneNumber.otps
        correct_otp = otps.get(phone_number) # دقت کنم که قبل از پاک کردن مقدار توش باید ذخیره اش کنم. 
        # اگه جای این خط و دستور بعد رو عوض کنم، اطلاعات این هم پاک میشه. چون هر دو به یه جای حافظه
        # اشاره میکنن. البته میشه تو کپی هم نگه داشت. اما چون یکبار مصرف هست و دیگه بهش کاری نداریم،
        # پاکش کردم. میتونم بعدا با ترد درست کنم که مثلا تا ۲ دقیقه نگه داره و اگه طرف دوباره خواست
        # براش نفرستم.
        del LoginWithPhoneNumber.otps[phone_number]
        if correct_otp==sent_otp:
            try:
                if username==None:
                    # new_user = get_user_model().objects.create(username=phone_number, phone_number=phone_number)
                    new_user = get_user_model().objects.create(username=phone_number, phone_number=phone_number)
                    PhoneNumber.objects.create(user=new_user, phone_number=phone_number)
                    login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                    context = {
                        'phone_number': phone_number
                    }
                    return render(request, 'register_with_phone_number.html', context)

            except IntegrityError:
                messages.error(request, _("Sorry! This phone number already has an account. If it's yours and you can't use it, contact the moderator of the site."))
            messages.success(request, _("Successfull Login."))
            return redirect('homepage')
            # context = {
            #     'phone_number': phone_number,
            # }
            # return render(request, 'index.html', context)
        else:
            messages.error(request, _("Sorry. OTP is invalid!"))
            return redirect('account_login')


class RegisterWithPhoneNumber(generic.TemplateView):
    template_name = 'register_with_phone_number.html'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        v = request.POST.get('verified')
        if v=='1': # یعنی تیک این رو زده که نمیخواد اطلاعاتش رو وارد کنه و از دفعه بعد هم نمیخواد ببینه این صفحه ره. پس تایید کرده و وریفاید رو ترو میذارم.
            username = request.POST.get('username')
            temp = PhoneNumber.objects.get(phone_number=username)
            temp.verified=True
            temp.save()
            messages.success(request, _("Your choice accepted successfully! That page won't be shown to you next time!"))
        else: # یعنی رو دکمه تایید نزده. اما شاید بخواد دفعه بعد بزنه. از طرفی شاید هم فرم اول رو پر کرده و میخواد اطلاعات رو وارد کنه. پس بررسی میکنیم.
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if username and email and password: # یعنی اگه یوزرنیم و ایمیل وارد کرده بود، پس میخواد تغییر بده
                form = forms.ChangeUserInfoAfterRegisterationForm(request.POST)
                phone_number = request.user.username
                if form.is_valid():
                    with transaction.atomic():
                        cleaned_data = form.cleaned_data
                        temp = PhoneNumber.objects.get(phone_number=phone_number)
                        temp.verified=True
                        temp.save()
                        user = get_user_model().objects.get(username=phone_number)
                        user.username=cleaned_data['username']
                        user.email = cleaned_data['email']
                        user.password = make_password(cleaned_data['password']) # خود جنگو ساده رو قبول نمیکنه. با این میشه هشش کرد.
                        user.phone_number = phone_number
                        user.save()
                        messages.success(request, _("Your info updated successfully! That page won't be shown to you next time!"))
                else:
                    messages.error(request, form.errors)
                    context = {
                        'phone_number': phone_number
                    }
                    return render(request, 'register_with_phone_number.html', context)
            else:
                messages.error(request, _("Your must enter all required fields!"))

        return redirect('homepage')