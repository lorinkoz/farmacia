# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-26 05:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0029_auto_20180124_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devueltocama',
            name='justificacion',
            field=models.CharField(choices=[('CAMBIO DE TRATAMIENTO', 'CAMBIO DE TRATAMIENTO'), ('TRASLADO', 'TRASLADO'), ('OTRA', 'OTRA'), ('FALLECIMIENTO', 'FALLECIMIENTO'), ('EGRESO', 'EGRESO')], max_length=40),
        ),
        migrations.AlterField(
            model_name='devueltofarmacia',
            name='justificacion',
            field=models.CharField(choices=[('VENCIMIENTO', 'VENCIMIENTO'), ('DISMINUCION DEL FONDO FIJO', 'DISMINUCION DEL FONDO FIJO'), ('RETENIDO', 'RETENIDO'), ('MAL ESTADO', 'MAL ESTADO')], max_length=40),
        ),
    ]
