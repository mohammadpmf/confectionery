from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, login
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin

from requests.exceptions import ConnectTimeout, SSLError
import ghasedakpack
import random, string, time, threading

from config.madval1369_secret import *
from .models import PhoneNumber, ProfilePicture
from . import forms
from cart.madval_functions import save_cart_in_db


sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)
good_line_number_for_sending_otp = '30005088' # مال خودم رو که میذارم، شانسی از این شماره یا 20008580 میفرسته که شماره ۳۰۰۰ اوکی هست. ولی ۲۰۰۰ داغانه یه بار تقریبا ۲۰ دقیقه طول کشید تا بفرسته که خب دیگه یکبار رمز به درد بخوری نیست.


class MadvalLogout(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        cart = self.request.session.get('cart')
        user = self.request.user
        if user.is_authenticated: # حتی اینجا هم لازمه که باشه. چون شاید طرف لاگین نیست و کرم داره الکی رو دکمه لاگ اوت بزنه. پس برای این که مشکل پیش نیاد اینجا هم شرط رو بررسی میکنیم.
            save_cart_in_db(user, cart)
        return redirect('account_logout')


class LogoutConfirm(generic.TemplateView):
    template_name = 'account/logout.html'


class LoginWithPhoneNumber(generic.TemplateView):
    otps = dict() # توی تابع اینیت که مینوشتم درست کار نمیکرد. اما اینجا به عنوان کلاس اتربیوت در نظر
    # گرفتم جواب داد. با این حال رو استرینگ کار نمیکرد. اما روی دیکشنری و لیست و مجموعه که به یه
    # جای حافظه اشاره میکنن با سلف دسترسی داشتم و میتونستم تو متد گت مقدار رمز رو ذخیره کنم و تو
    # متد پست ببینم یکی هست یا نه. اما برای استرینگ نمیشد. برای استرینگ هم به جای این که با سلف
    # صداش کنم با اسم کلاس صداش کردم درست شد. به خاطر همین برای همین متغیر او تی پیز که قراره رمزهای
    # یکبار مصرف رو نگه داره، با این که سلف اینجا کار رو دیکشنری جواب داد، با اسم کلاس صداش کردم.
    # باز هم میگم تو اینیت نوشتم جواب نمیداد. یعنی بعد از این که متد گت صدا میشد و تغییرش میدادم،
    # وقتی میرفتم تو متد پست اون مقدار نبود و یه دیکشنری خالی بود دوباره.

    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get('phone_number')
        if phone_number==None:
            messages.error(request, _("It seems you have not filled the phone number field! Please fill it"))
            return redirect('account_login')
        if phone_number.isalpha() or len(phone_number)!=11:
            messages.error(request, _("Phone number should be exactly 11 digits to get verification code"))
            return redirect('account_login')
        otp = str(random.randint(100000, 999999))
        messages.warning(request, f"otp is {otp}😊")
        username = PhoneNumber.objects.select_related('user').filter(phone_number=phone_number).first() # اگه باشه که میده. اگه نباشه نان میده
        LoginWithPhoneNumber.otps[phone_number]={
            'otp': otp,
            'username': username,
        }
        context = {
            'username': username,
            'phone_number': phone_number,
        }
        try:
            # answer = sms.verification({'receptor': phone_number, 'linenumber': good_line_number_for_sending_otp,'type': '1', 'template': MY_TEMPLATE_NAME_IN_GHASEDAK_ME_SITE, 'param1': otp})
            answer = True
            if answer:
                messages.success(request, "یک پیامک برای شماره %s ارسال شد. لطفا کد ارسال شده را جهت ادامه وارد کنید." %phone_number)
                return render(request, 'login_with_phone_number.html', context)
            messages.error(request, _("A problem occured in sending message. Please try again in a few minutes."))
            return redirect('account_login')
        except ConnectTimeout as error:
            messages.error(request, _("A problem occured in sms message server. Please try again in a few minutes."))
            messages.error(request, error)
            return redirect('account_login')
        except SSLError as error:
            messages.error(request, _("A problem occured which is related to SSL. Please check your VPN status or proxy settings!"))
            messages.error(request, error)
            return redirect('account_login')
        except ConnectionError as error:
            messages.error(request, _("A connection error occured. Please check your Internet!"))
            messages.error(request, error)
            return redirect('account_login')
        finally:
            threading.Thread(target=self.expire_sent_otp, args=(phone_number, )).start()

    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get('phone_number')
        sent_otp = request.POST.get('otp')
        otps = LoginWithPhoneNumber.otps
        current_user = otps.get(phone_number) # اگه طرف شماره رو انگولک نکرده باشه از تو اچ تی ام ال
        # یا مدت زمان منقضی نشده باشه، پس تو سرور این یه مقدار داره که یه دیکشنری هست و کلیدهای
        # otp, username داخلش هست و میتونیم از توش در بیاریم و کار دلخواه رو انجام بدیم
        # otp که رمز هست برای بررسی درستی استفاده میکنیم. یوزرنیم هم که اسمی هست که براش میسازیم
        # و تازه هست و مهم نیست. چون همون لحظه بهش میگیم اگه نمیخواد تغییرش بده. اما کدها رو طوری
        # نوشتم که ترجیحا همون شماره موبایل باشه. اگه اکانتی از قبل بوده تهش یه چیز رندوم اضافه کنه.
        if current_user == None: # یعنی یا منقضی شده و یا طرف دستکاری کرده فرم رو با اچ تی ام ال
            messages.error(request, _("OTP has been expired!"))
            return redirect('account_login')
        correct_otp = current_user.get('otp')
        username = current_user.get('username')
        # دقت کنم که قبل از پاک کردن مقدار توش باید ذخیره اش کنم این مقادیر رو.
        # اگه جای این خط و دستور بعد رو عوض کنم، اطلاعات این هم پاک میشه. چون هر دو به یه جای حافظه
        # اشاره میکنن. البته میشه تو کپی هم نگه داشت. اما چون یکبار مصرف هست و دیگه بهش کاری نداریم،
        # پاکش کردم. میتونم بعدا با ترد درست کنم که مثلا تا ۲ دقیقه نگه داره و اگه طرف دوباره خواست
        # براش نفرستم.
        try:
            del LoginWithPhoneNumber.otps[phone_number]
        except: # ممکنه اکسپایر شده باشه یا نباشه تو دیکشنری یا به هر دلیلی. به هر حال میگم ارور نده. سعی کن پاکش کنی. شد شد نشد نشد ولش کن😁
            pass
        if correct_otp==sent_otp:
            try:
                # if username=="None": # اول با اچ تی ام ال ارسال کرده بودم که کار درستی نبود. جدای از اون هم نان رو به استرینگ نان تبدیل میکرد گمج
                if username==None: # پس دفعه اول هست و میخواد اکانت بسازه
                    # ممکنه یه نفر قبلا یه یوزر ساخته و یه شماره موبایل الکی به عنوان یوزرنیمش گذاشته
                    # و این طوری کسی که واقعا با اون شماره موبایل بخواد ثبت نام کنه نمیتونه. چون
                    # همچین یوزرنیمی از قبل وجود داره. پس تو این حالت ته شماره اش یه چیز شانسی
                    # خودم اضافه میکنم. البته تو حالت طبیعی مشکلی نیست و با همون شماره باید بشه
                    # یوزرنیم ساخت که من این کار رو کردم. با این حال باز هم تو ترای و اکسپت گذاشتم😊
                    random_username = phone_number 
                    not_ok = get_user_model().objects.filter(username=random_username).first()
                    while not_ok:
                        random_username = phone_number+str(''.join(random.choices(string.ascii_letters+string.digits,k=random.randint(8, 10))))
                        not_ok = get_user_model().objects.filter(username=random_username).first()
                    new_user = get_user_model().objects.create(username=random_username, phone_number=phone_number)
                    PhoneNumber.objects.create(user=new_user, phone_number=phone_number)
                    login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                else: # قبلا حداقل یه بار وارد شده. پس اکانت داره
                    user = get_user_model().objects.get(username=username)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    temp = PhoneNumber.objects.get(phone_number=phone_number)
                    if temp.verified:
                        messages.success(request, "خوش آمدی %s" %username)
                        return redirect('homepage')
                context = {'phone_number': phone_number}
                messages.success(request, _("Successfull Login."))
                return render(request, 'register_with_phone_number.html', context)
            except IntegrityError:
                messages.error(request, _("Sorry! This phone number already has an account. If it's yours and you can't use it, contact the moderator of the site."))
                return redirect('account_login')
        else:
            messages.error(request, _("Sorry. OTP is invalid!"))
            return redirect('account_login')

    def expire_sent_otp(self, phone_number):
        time.sleep(120)
        try:
            del LoginWithPhoneNumber.otps[phone_number]
        except:
            pass


class RegisterWithPhoneNumber(generic.TemplateView):
    template_name = 'register_with_phone_number.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        v = request.POST.get('verified')
        user = request.user
        if v=='1': # یعنی تیک این رو زده که نمیخواد اطلاعاتش رو وارد کنه و از دفعه بعد هم نمیخواد ببینه این صفحه رو. پس تایید کرده و وریفاید رو ترو میذارم.
            temp = PhoneNumber.objects.get(user=user)
            temp.verified=True
            temp.save()
            messages.success(request, _("Your choice accepted successfully! That page won't be shown to you next time!"))
        else: # یعنی رو دکمه تایید نزده. اما شاید بخواد دفعه بعد بزنه. از طرفی شاید هم فرم اول رو پر کرده و میخواد اطلاعات رو وارد کنه. پس بررسی میکنیم.
            email = request.POST.get('email')
            password = request.POST.get('password')
            if email and password: # یعنی اگه ایمیل و پسورد وارد کرده بود، پس میخواد تغییر بده
                form = forms.ChangeUserInfoAfterRegisterationForm(request.POST)
                if form.is_valid():
                    with transaction.atomic():
                        cleaned_data = form.cleaned_data
                        temp = PhoneNumber.objects.get(user=user)
                        temp.verified=True
                        temp.save()
                        user.email = cleaned_data['email']
                        user.password = make_password(cleaned_data['password']) # خود جنگو ساده رو قبول نمیکنه. با این میشه هشش کرد.
                        user.save()
                        messages.success(request, _("Your info updated successfully! Please login again!"))
                else:
                    messages.error(request, form.errors)
                    return render(request, 'register_with_phone_number.html')
            else: # یعنی نمیخواست یوزرنیم و ایمیل و پسورد وارد کنه و بدون زدن اون تیک زده که الان فقط نمیخواد صفحه رو ببینه.
                messages.success(request, _("Ok. You are in a hurry! We will show you this form next time."))
        return redirect('homepage')


class ChangeProfile(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        form = forms.ChangeUserProfileInWebsiteForm(instance=request.user)
        profile_picture = ProfilePicture.objects.filter(user=request.user).first()
        context = {"form": form, "profile_picture": profile_picture}
        return render(request, 'change_user_info.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = forms.ChangeUserProfileInWebsiteForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            new_image = request.FILES.get('profile_picture')
            remove_profile_picture = request.POST.get('remove_profile_picture')
            form.save()
            if remove_profile_picture:
                prev_image = ProfilePicture.objects.filter(user=user).first()
                if prev_image:
                    prev_image.delete()
            else:
                if new_image:
                    prev_image = ProfilePicture.objects.filter(user=user).first()
                    if prev_image:
                        prev_image.image=new_image
                        prev_image.save()
                    else:
                        ProfilePicture.objects.create(user=user, image=new_image)
            messages.success(request, _("Information has been updated successfully!"))
            return redirect('homepage')
        else:
            messages.error(request, form.errors)
            return self.get(request, *args, **kwargs) # دیدم اینجا کار تکراری دارم میکنم. همون کارهای گت رو انجام میدادم. به جاش اون رو صدا کردم.


class ChangeUsername(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        form = forms.ChangeUsersUsernameInWebsiteForm(instance=request.user)
        context = {"form": form}
        return render(request, 'change_users_username.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = forms.ChangeUsersUsernameInWebsiteForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Username updated successfully!"))
            return redirect('homepage')
        else:
            messages.error(request, form.errors)
            return self.get(request, *args, **kwargs)


class ChangeEmailAddress(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        form = forms.ChangeUsersEmailAddressInWebsiteForm(instance=request.user)
        context = {"form": form}
        return render(request, 'change_users_email.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = forms.ChangeUsersEmailAddressInWebsiteForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Email address updated successfully!"))
            return redirect('homepage')
        else:
            messages.error(request, form.errors)
            return self.get(request, *args, **kwargs)


class ChangeOTPNumber(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        form = forms.ChangeUsersOTPNumberInWebsiteForm(instance=request.user)
        context = {"form": form}
        return render(request, 'change_users_otp_number.html', context)


class ChangeOTPNumberConfirm(LoginRequiredMixin, generic.TemplateView):
    otps = dict()

    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get('otp_phone_number')
        if phone_number.isalpha() or len(phone_number)!=11:
            messages.error(request, _("Phone number should be exactly 11 digits to get verification code"))
            return redirect('change_otp_number')
        is_registered = PhoneNumber.objects.filter(phone_number=phone_number).first()
        if is_registered:
            messages.error(request, _("This phone number is already registered!"))
            return redirect('change_otp_number')
        otp = str(random.randint(100000, 999999))
        messages.warning(request, f"otp is {otp}😊")
        ChangeOTPNumberConfirm.otps[request.user]={ # این دفعه چون اکانت داره از قبل، دیگه به شماره اش کاری نداریم و تو دیکشنری کلیدش رو یوزرنیمیش میذاریم
            'otp': otp,
            'phone_number': phone_number
        }
        context = {
            'phone_number': phone_number,
        }
        try:
            # وقتی اسم برای اکانت میذاشتم ارور میداد و سایت قاصدک آی پی لیمیتد مینوشت. اما با همون شماره کار کرد ولی دیر میومد و تو سایتش هم مینوشت در حال بررسی. شاید واقعا نگاه میکردن که کلمه عزیز برای کی به کار رفته. به هر حال کد من درست بود. اما دردسر زیاد داشت و و از همون اولی استفاده کردم تا اطلاع ثانوی
            # answer = sms.verification({'receptor': phone_number, 'linenumber': good_line_number_for_sending_otp,'type': '1', 'template': MY_TEMPLATE_NAME_IN_GHASEDAK_ME_SITE_TO_CHANGE_OTP_NUMBER, 'param1': request.user.get_name(), 'param2': phone_number, 'param3': otp})
            # answer = sms.verification({'receptor': phone_number, 'linenumber': good_line_number_for_sending_otp,'type': '1', 'template': MY_TEMPLATE_NAME_IN_GHASEDAK_ME_SITE, 'param1': otp})
            answer = True
            if answer:
                messages.success(request, "یک پیامک برای شماره %s ارسال شد. لطفا کد ارسال شده را جهت ادامه وارد کنید." %phone_number)
                return render(request, 'change_users_otp_number_confirm.html', context)
            messages.error(request, _("A problem occured in sending message. Please try again in a few minutes."))
            return redirect('change_otp_number')
        except ConnectTimeout as error:
            messages.error(request, _("A problem occured in sms message server. Please try again in a few minutes."))
            messages.error(request, error)
            return redirect('change_otp_number')
        except SSLError as error:
            messages.error(request, _("A problem occured which is related to SSL. Please check your VPN status or proxy settings!"))
            messages.error(request, error)
            return redirect('change_otp_number')
        except ConnectionError as error:
            messages.error(request, _("A connection error occured. Please check your Internet!"))
            messages.error(request, error)
            return redirect('change_otp_number')
        finally:
            threading.Thread(target=self.expire_sent_otp, args=(request.user, )).start()

    def post(self, request, *args, **kwargs):
        user = request.user
        sent_otp = request.POST.get('otp')
        otps = ChangeOTPNumberConfirm.otps
        current_user = otps.get(user)
        if current_user == None: # یعنی یا منقضی شده و یا طرف دستکاری کرده فرم رو با اچ تی ام ال
            messages.error(request, _("OTP has been expired!"))
            return redirect('change_otp_number')
        correct_otp = current_user.get('otp')
        phone_number = current_user.get('phone_number')
        try:
            del ChangeOTPNumberConfirm.otps[user]
        except: # ممکنه اکسپایر شده باشه یا نباشه تو دیکشنری یا به هر دلیلی. به هر حال میگم ارور نده. سعی کن پاکش کنی. شد شد نشد نشد ولش کن😁
            pass
        if correct_otp==sent_otp:
            with transaction.atomic():
                temp = PhoneNumber.objects.filter(user=user).first()
                if temp: # تو حالتی که اول طرف شماره موبایل ثبت نکرده باشه، ارور میداد. پس باید بسازیم براش.
                    temp.phone_number=phone_number
                    temp.save()
                else:
                    PhoneNumber.objects.create(user=user, phone_number=phone_number, verified=True)
                user.phone_number=phone_number
                user.save()
                messages.success(request, _("OTP Phone number updated successfully!"))
            return redirect('homepage')
        else:
            messages.error(request, _("Sorry. OTP is invalid!"))
            return redirect('change_otp_number')


    def expire_sent_otp(self, user):
        time.sleep(120)
        try:
            del ChangeOTPNumberConfirm.otps[user]
        except:
            pass
