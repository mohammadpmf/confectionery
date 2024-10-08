# Generated by Django 5.0.7 on 2024-07-30 18:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nat_code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(10, 'National code must be exactly 10 digits'), django.core.validators.MaxLengthValidator(10, 'National code must be exactly 10 digits')], verbose_name='National Code'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(11, 'Phone number should be at least 11 digits'), django.core.validators.MaxLengthValidator(14, 'Phone number should be at most 14 digits')], verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11, 'Phone number must be at exactly 11 digits in Iran to receive sms'), django.core.validators.MaxLengthValidator(11, 'Phone number must be at exactly 11 digits in Iran to receive sms')], verbose_name='Phone number'),
        ),
    ]
