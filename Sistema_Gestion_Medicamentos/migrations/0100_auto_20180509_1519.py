# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-09 19:19
from __future__ import unicode_literals

import Sistema_Gestion_Medicamentos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0099_auto_20180509_1516'),
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
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
    ]
