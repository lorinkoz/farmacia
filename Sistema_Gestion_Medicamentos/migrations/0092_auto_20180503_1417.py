# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-03 18:17
from __future__ import unicode_literals

import Sistema_Gestion_Medicamentos.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0091_auto_20180503_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='devueltoalmacen',
            name='servicio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Sala'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoalmacen',
            name='servicio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Sala'),
            preserve_default=False,
        ),
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
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
    ]
