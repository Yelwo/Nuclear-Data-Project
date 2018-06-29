# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isotopes', '0003_auto_20171204_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='isotope',
            name='a_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='isotope',
            name='atomic_mass',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='isotope',
            name='binding_energy',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='isotope',
            name='natural_abund',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='isotope',
            name='z_number',
            field=models.IntegerField(default=0),
        ),
    ]
