# Generated by Django 5.0.7 on 2024-08-01 16:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_phonenumber_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='otp_phone_number', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]