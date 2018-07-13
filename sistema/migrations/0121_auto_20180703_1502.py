# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-07-03 19:02
from __future__ import unicode_literals

import sistema.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sistema', '0120_auto_20180703_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[sistema.models.validar]),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[sistema.models.validar]),
        ),
        migrations.RemoveField(
            model_name='permisoglobal',
            name='secretaria_sala',
        ),
        migrations.AddField(
            model_name='permisoglobal',
            name='secretaria_sala',
            field=models.ManyToManyField(blank=True, related_name='secretaria_sala', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[sistema.models.validar]),
        ),
    ]
