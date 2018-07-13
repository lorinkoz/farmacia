# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-26 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0032_auto_20180126_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='devueltosaladetalle',
            name='producto',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidosaladetalle',
            name='producto',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='devueltocama',
            name='justificacion',
            field=models.CharField(choices=[('FALLECIMIENTO', 'FALLECIMIENTO'), ('OTRA', 'OTRA'), ('EGRESO', 'EGRESO'), ('TRASLADO', 'TRASLADO'), ('CAMBIO DE TRATAMIENTO', 'CAMBIO DE TRATAMIENTO')], max_length=40),
        ),
        migrations.AlterField(
            model_name='devueltofarmacia',
            name='justificacion',
            field=models.CharField(choices=[('MAL ESTADO', 'MAL ESTADO'), ('VENCIMIENTO', 'VENCIMIENTO'), ('RETENIDO', 'RETENIDO'), ('DISMINUCION DEL FONDO FIJO', 'DISMINUCION DEL FONDO FIJO')], max_length=40),
        ),
    ]
