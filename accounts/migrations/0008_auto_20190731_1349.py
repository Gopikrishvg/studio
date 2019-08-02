# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-31 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190731_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='premiumbooking',
            name='premium_id',
        ),
        migrations.AddField(
            model_name='premiumbooking',
            name='user_premium',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='premiumbooking',
            name='premium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Premium'),
        ),
    ]
