# Generated by Django 5.0.7 on 2024-08-06 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confectionery', '0007_suggestionscritics_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Time Created')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Last Time Edited')),
            ],
        ),
    ]
