# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-16 11:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isotopes', '0010_auto_20180116_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='isotope',
            name='_germ',
        ),
        migrations.RemoveField(
            model_name='isotope',
            name='_iso_id',
        ),
    ]
