from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price', ]
    extra=1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['user', 'first_name', 'last_name', 'datetime_created', 'is_paid', ]
    list_display_links = ['user', 'first_name', 'last_name', 'datetime_created', 'is_paid', ]
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ['order', 'product', 'quantity', 'price', ]
    list_display_links = ['order', 'product', 'quantity', 'price', ]
