# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-31 10:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190731_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premiumbooking',
            name='premium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Premium'),
        ),
        migrations.AlterField(
            model_name='premiumbooking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='premiumbook', to=settings.AUTH_USER_MODEL),
        ),
    ]
