# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-04-25 18:31
from __future__ import unicode_literals

import sistema.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0087_auto_20180425_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedidofarmacia',
            options={'ordering': ['nombre']},
        ),
        migrations.RemoveField(
            model_name='devueltosala',
            name='entidad',
        ),
        migrations.RemoveField(
            model_name='pedidofarmacia',
            name='entidad',
        ),
        migrations.RemoveField(
            model_name='pedidosala',
            name='entidad',
        ),
        migrations.AddField(
            model_name='devueltofarmacia',
            name='devuelto_almacen_detalle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.DevueltoAlmacenDetalle'),
        ),
        migrations.AddField(
            model_name='pedidofarmacia',
            name='nombre',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, validators=[sistema.models.validar]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, validators=[sistema.models.validar]),
        ),
        migrations.DeleteModel(
            name='Entidad',
        ),
    ]
