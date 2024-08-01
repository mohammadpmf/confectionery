# Generated by Django 5.0.7 on 2024-07-30 13:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confectionery', '0004_productananymoususercomment_productcustomusercomment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='productananymoususercomment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='is approved'),
        ),
        migrations.AlterField(
            model_name='productcustomusercomment',
            name='dont_show_my_name',
            field=models.BooleanField(default=False, verbose_name="don't show my name"),
        ),
        migrations.AlterField(
            model_name='productcustomusercomment',
            name='is_approved',
            field=models.BooleanField(default=True, verbose_name='is approved'),
        ),
        migrations.AlterField(
            model_name='productcustomusercomment',
            name='stars',
            field=models.IntegerField(blank=True, choices=[(5, 'fantastic'), (4, 'excellent'), (3, 'good'), (2, 'average'), (1, 'bad')], null=True, verbose_name="user's rate"),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_users', to='confectionery.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_products', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'unique_together': {('product', 'user')},
            },
        ),
    ]