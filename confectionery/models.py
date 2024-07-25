from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

class Product(models.Model):
    PRODUCT_TYPE_CHOICES_CAKE = 'cake'
    PRODUCT_TYPE_CHOICES_PASTRY = 'pastry'
    PRODUCT_TYPE_CHOICES_BREAD = 'bread'
    PRODUCT_TYPE_CHOICES = (
        (PRODUCT_TYPE_CHOICES_CAKE, _('Cake')),
        (PRODUCT_TYPE_CHOICES_PASTRY, _('Pastry')),
        (PRODUCT_TYPE_CHOICES_BREAD, _('Bread')),
    )
    FLOUR_TYPE_CHOICES_WHEAT = 'wheat'
    FLOUR_TYPE_CHOICES_CORN = 'corn'
    FLOUR_TYPE_CHOICES_RICE = 'rice'
    FLOUR_TYPE_CHOICES = (
        (FLOUR_TYPE_CHOICES_WHEAT, _('Wheat')),
        (FLOUR_TYPE_CHOICES_CORN, _('Corn')),
        (FLOUR_TYPE_CHOICES_RICE, _('Rice')),
    )
    FAT_SUGRE_RATE_CHOICES_HIGH = 'high'
    FAT_SUGRE_RATE_CHOICES_AVERAGE = 'avg'
    FAT_SUGRE_RATE_CHOICES_LOW = 'low'
    FAT_SUGRE_RATE_CHOICES = (
        (FAT_SUGRE_RATE_CHOICES_HIGH, _('High')),
        (FAT_SUGRE_RATE_CHOICES_AVERAGE, _('Average')),
        (FAT_SUGRE_RATE_CHOICES_LOW, _('Low')),
    )

    title = models.CharField(verbose_name=_('Title'), max_length=255)
    product_type = models.CharField(verbose_name=_('Product Type'), max_length=8, choices=PRODUCT_TYPE_CHOICES)
    flour_type = models.CharField(verbose_name=_('Flour Type'), max_length=8, choices=FLOUR_TYPE_CHOICES)
    sugar_rate = models.CharField(verbose_name=_('Sugar Rate'), max_length=8, choices=FAT_SUGRE_RATE_CHOICES)
    fat_rate = models.CharField(verbose_name=_('Fat Rate'), max_length=8, choices=FAT_SUGRE_RATE_CHOICES)
    slug = models.SlugField(verbose_name=_('Slug'), )
    weight = models.DecimalField(verbose_name=_('Weight'), max_digits=3, decimal_places=1)
    price_toman = models.PositiveIntegerField(verbose_name=_('Price Toman'), )
    preparation_time = models.PositiveSmallIntegerField(verbose_name=_('Preparation Time'), validators=[MaxValueValidator(10)])
    ingredients = models.CharField(verbose_name=_('Ingredients'), max_length=1024)
    expiration_days = models.PositiveSmallIntegerField(verbose_name=_('Expiration Days'), default=3, validators=[MaxValueValidator(60)])
    main_image = models.ImageField(verbose_name=_('Main Image'), upload_to='main_images/', blank=True)
    extra_information = models.TextField(verbose_name=_('Extra Information'), max_length=10000, blank=True)
    # likes Foreign key
    # comments Foreign key
    # extra_images Foreign key
    # extra_films Foreign key

    def __str__(self):
        return f"{self.title} {self.weight}{_('grs')} {_('Price')}: {self.price_toman} {_('Toman')}"
