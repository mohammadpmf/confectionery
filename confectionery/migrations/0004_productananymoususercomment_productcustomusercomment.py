# Generated by Django 5.0.7 on 2024-07-29 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confectionery', '0003_productimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAnanymousUserComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000, verbose_name='comment text')),
                ('author', models.CharField(max_length=255, verbose_name='author')),
                ('is_approved', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anonymous_comments', to='confectionery.product', verbose_name='product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCustomUserComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000, verbose_name='comment text')),
                ('is_approved', models.BooleanField(default=True)),
                ('dont_show_my_name', models.BooleanField(default=False)),
                ('stars', models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='confectionery.product', verbose_name='product')),
            ],
        ),
    ]
