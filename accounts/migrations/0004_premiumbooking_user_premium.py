# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-31 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190731_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiumbooking',
            name='user_premium',
            field=models.BooleanField(default=False),
        ),
    ]