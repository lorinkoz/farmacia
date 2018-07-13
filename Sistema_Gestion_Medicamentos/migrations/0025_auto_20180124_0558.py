# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-24 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0024_auto_20180124_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devueltocama',
            name='justificacion',
            field=models.CharField(choices=[('OTRA', 'OTRA'), ('TRASLADO', 'TRASLADO'), ('CAMBIO DE TRATAMIENTO', 'CAMBIO DE TRATAMIENTO'), ('FALLECIMIENTO', 'FALLECIMIENTO'), ('EGRESO', 'EGRESO')], max_length=40),
        ),
        migrations.AlterField(
            model_name='devueltofarmacia',
            name='justificacion',
            field=models.CharField(choices=[('VENCIMIENTO', 'VENCIMIENTO'), ('RETENIDO', 'RETENIDO'), ('DISMINUCION DEL FONDO FIJO', 'DISMINUCION DEL FONDO FIJO'), ('MAL ESTADO', 'MAL ESTADO')], max_length=40),
        ),
        migrations.AlterField(
            model_name='pedidosaladetalle',
            name='cantidad_entregada',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
