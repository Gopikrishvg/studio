# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-31 13:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_premiumbooking_user_premium'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='premiumbooking',
            name='user_premium',
        ),
    ]
