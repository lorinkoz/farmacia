# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-23 06:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0013_auto_20180131_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevueltoCama',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('historia_clinica', models.IntegerField()),
                ('dosis', models.FloatField()),
                ('unidad_medida', models.CharField(choices=[('mg', 'mg'), ('g', 'g'), ('mL', 'mL'), ('%', '%'), ('L', 'L')], max_length=5)),
                ('cantidad_devuelta', models.IntegerField()),
                ('justificacion', models.CharField(choices=[('Otra', 'Otra'), ('Fallecimiento', 'Fallecimiento'), ('Cambio de tratamiento', 'Cambio de tratamiento'), ('Dado de alta', 'Dado de alta'), ('Traslado', 'Traslado')], max_length=40)),
                ('medico', models.CharField(max_length=40)),
                ('cama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Cama')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='TarjetaEstiba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fondo_fijo', models.IntegerField()),
                ('entrada', models.IntegerField()),
                ('salida', models.IntegerField()),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Producto')),
            ],
        ),
        migrations.RemoveField(
            model_name='devuelto',
            name='cama',
        ),
        migrations.RemoveField(
            model_name='devuelto',
            name='producto',
        ),
        migrations.DeleteModel(
            name='Devuelto',
        ),
    ]
