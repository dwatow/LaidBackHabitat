# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-16 03:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderRoom', '0005_auto_20160515_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomsoforder',
            old_name='estimate_checkin_date',
            new_name='over_night_date',
        ),
        migrations.RemoveField(
            model_name='roomsoforder',
            name='estimate_checkout_date',
        ),
    ]
