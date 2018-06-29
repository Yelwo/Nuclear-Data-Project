# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-30 11:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('isotopes', '0013_nuclearstructuretable'),
    ]

    operations = [
        migrations.AddField(
            model_name='nuclearstructuretable',
            name='shell_16',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shell_16', to='isotopes.NeutProtTuple'),
        ),
        migrations.AddField(
            model_name='nuclearstructuretable',
            name='shell_17',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shell_17', to='isotopes.NeutProtTuple'),
        ),
    ]
