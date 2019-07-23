# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-22 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6, null=True),
        ),
    ]