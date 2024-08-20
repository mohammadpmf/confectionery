from django.contrib import admin

from . import models
from .madval_filters import PriceFilter, WeightFilter


class ProductAnanymousUserCommentAdminInline(admin.TabularInline):
    model = models.ProductAnanymousUserComment
    extra = 1


class ProductCustomUserCommentAdminInline(admin.TabularInline):
    model = models.ProductCustomUserComment
    extra = 1


class ProductImageAdminInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


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
    prepopulated_fields = {
        'slug': ['title', ]
    }
    inlines = [ProductImageAdminInline, ProductCustomUserCommentAdminInline, ProductAnanymousUserCommentAdminInline]


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = models.ProductImage
    list_display = ['id', 'product', 'image']
    list_display_links = ['id', 'product', 'image']


@admin.register(models.ProductAnanymousUserComment)
class ProductAnanymousUserCommentAdmin(admin.ModelAdmin):
    model = models.ProductAnanymousUserComment
    list_display = ['product', 'text', 'author', 'is_approved']
    list_display_links = ['product', 'text', 'author']
    list_editable = ['is_approved']


@admin.register(models.ProductCustomUserComment)
class ProductCustomUserCommentAdmin(admin.ModelAdmin):
    model = models.ProductCustomUserComment
    list_display = ['product', 'text', 'author', 'is_approved', 'dont_show_my_name', 'stars']
    list_display_links = ['product', 'text', 'author', 'dont_show_my_name', 'stars']
    list_editable = ['is_approved']


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    model = models.Favorite
    list_display = ['product', 'user']
    list_display_links = ['product', 'user']


@admin.register(models.SuggestionsCritics)
class SuggestionsCriticsAdmin(admin.ModelAdmin):
    model = models.SuggestionsCritics
    list_display = ['name', 'email', 'subject', 'datetime_created', 'seen']
    list_display_links = ['name', 'email', 'subject', 'datetime_created', 'seen']


@admin.register(models.NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    model = models.NewsLetter
    list_display = ['email']
    list_display_links = ['email']


@admin.register(models.Chef)
class ChefAdmin(admin.ModelAdmin):
    model = models.Chef
    list_display = ['name', 'talent', 'email', 'facebook', 'instagram', 'linkedin', 'twitter']
    list_display_links = ['name', 'talent', 'email', 'facebook', 'instagram', 'linkedin', 'twitter']
