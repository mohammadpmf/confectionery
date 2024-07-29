from django.contrib import admin

from . import models
from .madval_filters import PriceFilter, WeightFilter


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    model = models.Product
    list_display = ['id', 'title', 'weight', 'price_toman', 'preparation_time', 'expiration_days']
    list_display_links = ['id', 'title']
    list_editable = ['weight', 'price_toman', 'preparation_time', 'expiration_days']
    list_filter = ['product_type', 'flour_type', WeightFilter, PriceFilter]
    search_fields = ['title']
    list_per_page = 20
    ordering = ['id']
    save_on_top = True # بولین هست و تو صفحه جزییات، سیو و دیلیت و گزینه ها رو علاوه بر پایین صفحه، بالا هم میاره اگه بذاریم ترو. به صورت پیش فرض فالس هست.
    # prepopulated_fields = {
    #     'slug': ['title', ] بعدا که اسلاگ فارسی رو اضافه کردم این رو هم بذارم.
    # }


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = models.ProductImage
    list_display = ['id', 'product', 'image']
    list_display_links = ['id', 'product', 'image']