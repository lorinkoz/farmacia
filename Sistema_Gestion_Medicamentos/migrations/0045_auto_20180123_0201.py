# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-23 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0044_auto_20180128_0550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devueltofarmacia',
            name='tarjeta_estiba',
        ),
        migrations.RemoveField(
            model_name='tarjetaestiba',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='tarjetaestibadetalle',
            name='tarjeta_estiba',
        ),
        migrations.AlterField(
            model_name='devueltocama',
            name='justificacion',
            field=models.CharField(choices=[('OTRA', 'OTRA'), ('CAMBIO DE TRATAMIENTO', 'CAMBIO DE TRATAMIENTO'), ('TRASLADO', 'TRASLADO'), ('FALLECIMIENTO', 'FALLECIMIENTO'), ('EGRESO', 'EGRESO')], max_length=40),
        ),
        migrations.DeleteModel(
            name='DevueltoFarmacia',
        ),
        migrations.DeleteModel(
            name='TarjetaEstiba',
        ),
        migrations.DeleteModel(
            name='TarjetaEstibaDetalle',
        ),
    ]
