# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-24 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0020_auto_20180124_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devueltocama',
            name='justificacion',
            field=models.CharField(choices=[('EGRESO', 'EGRESO'), ('OTRA', 'OTRA'), ('TRASLADO', 'TRASLADO'), ('FALLECIMIENTO', 'FALLECIMIENTO'), ('CAMBIO DE TRATAMIENTO', 'CAMBIO DE TRATAMIENTO')], max_length=40),
        ),
        migrations.AlterField(
            model_name='devueltofarmacia',
            name='justificacion',
            field=models.CharField(choices=[('VENCIMIENTO', 'VENCIMIENTO'), ('MAL ESTADO', 'MAL ESTADO'), ('DISMINUCION DEL FONDO FIJO', 'DISMINUCION DEL FONDO FIJO'), ('RETENIDO', 'RETENIDO')], max_length=40),
        ),
        migrations.AlterField(
            model_name='pedidocama',
            name='pedido_sala_detalle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.PedidoSalaDetalle'),
        ),
    ]
