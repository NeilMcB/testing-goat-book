# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-04 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]