# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-01 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nucreactions', '0008_auto_20180422_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactionsfield',
            name='elementary_particle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reaction_elementary_particle', to='elementaryparticles.ElementaryParticle'),
        ),
        migrations.AlterField(
            model_name='reactionsfield',
            name='radiation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reaction_radiation', to='radiations.Radiation'),
        ),
        migrations.DeleteModel(
            name='ElementaryParticle',
        ),
        migrations.DeleteModel(
            name='Radiation',
        ),
    ]