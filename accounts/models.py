from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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
            MinValueValidator(10, _("National code must be exactly 10 digits")),
            MaxValueValidator(10, _("National code must be exactly 10 digits")),
        ],
    )
    gender = models.CharField(verbose_name=_('Gender'), max_length=1, blank=True, choices=GENDER_CHOICES)
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    phone_number = models.CharField(verbose_name=_('Phone number'), max_length=14,
        blank=True, null=True, unique=True, validators=[
        MinValueValidator(11, _("Phone number should be at least 11 digits")),
        MaxValueValidator(14, _("Phone number should be at most 14 digits"))
        ],
    )
