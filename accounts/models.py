from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    GENDER_FEMALE = 'f'
    GENDER_MALE = 'm'
    GENDER_CHOICES =(
        (GENDER_FEMALE, _('Female')),
        (GENDER_MALE, _('Male')),
    )

    nat_code = models.CharField(
        verbose_name=_('National Code'), max_length=10, blank=True, null=True, unique=True,
        validators=[
            MinLengthValidator(10, _("National code must be exactly 10 digits")),
            MaxLengthValidator(10, _("National code must be exactly 10 digits")),
        ],
    )
    gender = models.CharField(verbose_name=_('Gender'), max_length=1, blank=True, choices=GENDER_CHOICES)
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    phone_number = models.CharField(verbose_name=_('Phone number'), max_length=14,
        blank=True, null=True, unique=True, validators=[
        MinLengthValidator(11, _("Phone number should be at least 11 digits")),
        MaxLengthValidator(14, _("Phone number should be at most 14 digits"))
        ],
    )

    # def __str__(self): # اول این رو نوشتم. تو قسمت احراز هویت مشکل پیش اومد. چون بعضی جاها
    # متغیر یوزر رو مقایسه میکردم و به جای یوزر اسمش رو در نظر میگرفت. اما بعضی جاها که
    # اسم نداشت خود آبجکت رو. بگذریم. برای حل شدن سریع مشکل اسم تابع رو عوش کردم و کامل
    # تر هم کردم. این رو گذاشتم اینجا که یادم باشه.
    #     if self.first_name:
    #         return f"{self.first_name}"
    #     return super().__str__()
    def get_name(self):
        if self.first_name and self.last_name:
            return "%s %s" %(self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            if self.gender:
                if self.gender=="m":
                    return "آقای %s" %self.last_name
                elif self.gender=="f":
                    return "خانم %s" %self.last_name
            else:
                return self.last_name
        else:
            return "%s" %self.username


class PhoneNumber(models.Model):
    user = models.OneToOneField(verbose_name=_('User'), to=CustomUser, on_delete=models.CASCADE, related_name='otp_phone_number') # چون خود کاستومر ها فون نامبر دارن اما اختیاری هست. در واقع اون رو برای اطلاع رسانی میتونن استفاده کنن این فقط برای او تی پی که اگه دوست دارن خودشون میتونن هر دو تا رو یکی بذارن. به صورت پیش فرض خودم موقع ورود با او تی پی این کار رو میکنم. یعنی شماره اختیاری یوزر رو هم میذارم همین که اس ام اس های دیگه هم بره به اونجا. البته فقط موقع ثبت نام. از دفعات بعد دیگه این کار رو نمیکنم. کدهاش رو تو ویوز نوشتم.
    phone_number = models.CharField(verbose_name=_('Phone number'), max_length=11, unique=True, validators=[
        MinLengthValidator(11, _("Phone number must be at exactly 11 digits in Iran to receive sms")),
        MaxLengthValidator(11, _("Phone number must be at exactly 11 digits in Iran to receive sms"))
        ],)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


class ProfilePicture(models.Model):
    user = models.OneToOneField(verbose_name=_('User'), to=CustomUser, on_delete=models.CASCADE, related_name='profile_picture')
    image = models.ImageField(verbose_name=_('Image'), upload_to='profile_pictures/', )
