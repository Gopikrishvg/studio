# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-23 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_event_eventbooking_studio_studiobooking_studioimage_studiovideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='studio',
            name='cost_per_hour',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
