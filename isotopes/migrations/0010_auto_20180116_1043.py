# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-16 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isotopes', '0009_remove_isotope_iso_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='isotope',
            name='_germ',
            field=models.CharField(db_column='germ', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='isotope',
            name='_iso_id',
            field=models.CharField(db_column='iso_id', max_length=10, null=True),
        ),
    ]
