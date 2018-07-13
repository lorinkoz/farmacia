# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-09 19:16
from __future__ import unicode_literals

import Sistema_Gestion_Medicamentos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0098_auto_20180509_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.AlterField(
            model_name='pedidocama',
            name='cantidad_solicitada',
            field=models.IntegerField(validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
    ]
