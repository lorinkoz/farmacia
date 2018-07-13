# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-07-13 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import sistema.models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0122_auto_20180706_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[sistema.models.validar]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[sistema.models.validar]),
        ),
    ]
