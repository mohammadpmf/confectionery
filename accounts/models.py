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


class PhoneNumber(models.Model):
    user = models.OneToOneField(verbose_name=_('User'), to=CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name=_('Phone number'), max_length=11, validators=[
        MinLengthValidator(11, _("Phone number must be at exactly 11 digits in Iran to receive sms")),
        MaxLengthValidator(11, _("Phone number must be at exactly 11 digits in Iran to receive sms"))
        ],)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"
