# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-23 10:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isotopes', '0011_auto_20180116_1132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='isotope',
            options={'ordering': ['z_number', 'a_number']},
        ),
    ]