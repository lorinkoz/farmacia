# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-15 15:50
from __future__ import unicode_literals

import sistema.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0108_auto_20180515_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[sistema.models.validar]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[sistema.models.validar]),
        ),
    ]
