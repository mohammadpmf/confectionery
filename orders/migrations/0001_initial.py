# Generated by Django 5.0.7 on 2024-08-11 11:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('confectionery', '0010_alter_chef_facebook_alter_chef_instagram_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده؟')),
                ('first_name', models.CharField(max_length=255, verbose_name='نام')),
                ('last_name', models.CharField(max_length=255, verbose_name='نام خانوادگی')),
                ('phone_number', models.CharField(max_length=14, validators=[django.core.validators.MinLengthValidator(11, 'شماره تلفن باید حداقل ۱۱ رقم باشد'), django.core.validators.MaxLengthValidator(14, 'شماره تلفن باید حداکثر ۱۴ رقم باشد')], verbose_name='شماره تماس')),
                ('address', models.TextField(max_length=500, verbose_name='آدرس')),
                ('order_notes', models.TextField(blank=True, max_length=1000, verbose_name='یادداشت برای سفارش')),
                ('zarinpal_authority', models.CharField(blank=True, max_length=255)),
                ('zarinpal_ref_id', models.CharField(blank=True, max_length=255)),
                ('zarinpal_data', models.TextField(blank=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='زمان آخرین ویرایش')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='تعداد')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='ثبت سفارش')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='confectionery.product', verbose_name='محصول')),
            ],
        ),
    ]
