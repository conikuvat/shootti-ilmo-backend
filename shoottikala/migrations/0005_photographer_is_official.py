# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoottikala', '0004_auto_20170525_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographer',
            name='is_official',
            field=models.BooleanField(default=False, verbose_name='Tapahtuman virallinen valokuvaaja'),
        ),
    ]
