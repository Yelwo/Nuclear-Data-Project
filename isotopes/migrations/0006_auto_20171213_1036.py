# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 10:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('isotopes', '0005_auto_20171213_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unstable',
            name='child',
        ),
        migrations.AddField(
            model_name='isotope',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='isotopes.Isotope'),
        ),
    ]
