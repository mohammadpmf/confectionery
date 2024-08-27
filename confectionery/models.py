from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.utils.text import slugify


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
    FLOUR_TYPE_CHOICES_OAT = 'oat'
    FLOUR_TYPE_CHOICES = (
        (FLOUR_TYPE_CHOICES_WHEAT, _('Wheat')),
        (FLOUR_TYPE_CHOICES_CORN, _('Corn')),
        (FLOUR_TYPE_CHOICES_RICE, _('Rice')),
        (FLOUR_TYPE_CHOICES_OAT, _('Oat')),
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
    slug = models.SlugField(verbose_name=_('Slug'), allow_unicode=True, unique=True, db_collation='utf8_persian_ci')
    weight = models.DecimalField(verbose_name=_('Weight'), max_digits=3, decimal_places=1)
    price_toman = models.PositiveIntegerField(verbose_name=_('Price Toman'), )
    preparation_time = models.PositiveSmallIntegerField(verbose_name=_('Preparation Time'), validators=[MaxValueValidator(10)])
    ingredients = models.CharField(verbose_name=_('Ingredients'), max_length=1024)
    expiration_days = models.PositiveSmallIntegerField(verbose_name=_('Expiration Days'), default=3, validators=[MaxValueValidator(60)])
    main_image = models.ImageField(verbose_name=_('Main Image'), upload_to='main_images/', blank=True)
    extra_information = models.TextField(verbose_name=_('Extra Information'), max_length=10000, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk, "slug": self.slug})

    def __str__(self):
        return f"{self.title} {self.weight}{gettext('Kgs')} {gettext('Price')}: {self.price_toman} {gettext('Toman')}"


class ProductImage(models.Model):
    product = models.ForeignKey(verbose_name=_('product'), to=Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name=_('image'), upload_to='product_images/')


class ProductAnanymousUserComment(models.Model):
    product = models.ForeignKey(verbose_name=_('product'), to=Product, on_delete=models.CASCADE, related_name='anonymous_comments')
    text = models.TextField(verbose_name=_('comment text'), max_length=10000)
    author = models.CharField(verbose_name=_('author'), max_length=255)
    is_approved = models.BooleanField(verbose_name=_('is approved'), default=False)
    datetime_created = models.DateTimeField(verbose_name=_('Date Time Created'), auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.text}"


class ProductCustomUserComment(models.Model):
    STAR_CHOICES = (
        (5, _('fantastic')),
        (4, _('excellent')),
        (3, _('good')),
        (2, _('average')),
        (1, _('bad')),
    )

    product = models.ForeignKey(verbose_name=_('product'), to=Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name=_('comment text'), max_length=10000)
    author = models.ForeignKey(verbose_name=_('author'), to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(verbose_name=_('is approved'), default=True)
    dont_show_my_name = models.BooleanField(verbose_name=_("don't show my name"), default=False)
    stars = models.IntegerField(verbose_name=_("user's rate"), choices=STAR_CHOICES, null=True, blank=True)
    datetime_created = models.DateTimeField(verbose_name=_('Date Time Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(verbose_name=_('Last Time Edited'), auto_now=True)

    def __str__(self):
        full_name = f"{self.author.first_name} {self.author.last_name}".strip()
        if full_name=="":
            full_name = self.author
        return f"{full_name}: {self.text}"


class Favorite(models.Model):
    product = models.ForeignKey(verbose_name=_('product'), to=Product, on_delete=models.CASCADE, related_name='favorited_users')
    user = models.ForeignKey(verbose_name=_('user'), to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_products')
    
    class Meta:
        unique_together = ('product', 'user')


class SuggestionsCritics(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    email = models.EmailField(verbose_name=_('Email'), max_length=255)
    subject = models.CharField(verbose_name=_('Subject'), max_length=255)
    text = models.TextField(verbose_name=_('Text'), max_length=10000)
    seen = models.BooleanField(verbose_name=_('Seen'), default=False)
    datetime_created = models.DateTimeField(verbose_name=_('Date Time Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(verbose_name=_('Last Time Edited'), auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.subject}"


class NewsLetter(models.Model):
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)
    datetime_created = models.DateTimeField(verbose_name=_('Date Time Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(verbose_name=_('Last Time Edited'), auto_now=True)


class Chef(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    talent = models.CharField(verbose_name=_('Talent'), max_length=255)
    image= models.ImageField(verbose_name=_('Image'), upload_to='chef_images/', blank=True)
    description = models.TextField(verbose_name='description', max_length=10000, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=255, blank=True)
    facebook = models.CharField(verbose_name='Facebook', max_length=255, blank=True)
    instagram = models.CharField(verbose_name='Instagram', max_length=255, blank=True)
    linkedin = models.CharField(verbose_name='Linkedin', max_length=255, blank=True)
    twitter = models.CharField(verbose_name='Twitter', max_length=255, blank=True)
