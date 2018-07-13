# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-04-26 15:38
from __future__ import unicode_literals

import Sistema_Gestion_Medicamentos.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0088_auto_20180425_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoAlmacen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entregado_por', models.CharField(max_length=40)),
                ('recibido_por', models.CharField(max_length=40)),
                ('autorizado_por', models.CharField(max_length=40)),
                ('importe_enviada_total', models.FloatField(default=0)),
                ('importe_recibida_total', models.FloatField(default=0)),
                ('fecha_hora', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoAlmacenDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_enviada', models.IntegerField()),
                ('cantidad_recibida', models.IntegerField(blank=True, null=True)),
                ('importe_enviada', models.FloatField(default=0)),
                ('importe_recibida', models.FloatField(default=0)),
                ('saldo', models.IntegerField(blank=True, null=True)),
                ('pedido_almacen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_almacen', to='Sistema_Gestion_Medicamentos.PedidoAlmacen')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Producto')),
            ],
        ),
        migrations.AlterModelOptions(
            name='pedidofarmacia',
            options={'ordering': ['producto']},
        ),
        migrations.RemoveField(
            model_name='pedidofarmacia',
            name='nombre',
        ),
        migrations.AddField(
            model_name='pedidofarmacia',
            name='cantidad_enviada',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidofarmacia',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Producto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.AddField(
            model_name='pedidofarmacia',
            name='pedido_almacen_detalle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.PedidoAlmacenDetalle'),
        ),
    ]
