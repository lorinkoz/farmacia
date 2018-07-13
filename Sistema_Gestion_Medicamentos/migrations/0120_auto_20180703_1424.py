# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-07-03 18:24
from __future__ import unicode_literals

import Sistema_Gestion_Medicamentos.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Sistema_Gestion_Medicamentos', '0119_auto_20180703_1325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='farmacia',
            options={'ordering': ['centro_costo']},
        ),
        migrations.AddField(
            model_name='devueltoalmacen',
            name='farmacia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Farmacia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='farmacia',
            name='responsable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='responsable', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoalmacen',
            name='farmacia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sistema_Gestion_Medicamentos.Farmacia'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='farmacia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmacia', to='Sistema_Gestion_Medicamentos.Farmacia'),
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='sala',
        ),
        migrations.AddField(
            model_name='servicio',
            name='sala',
            field=models.ManyToManyField(blank=True, related_name='sala', to='Sistema_Gestion_Medicamentos.Sala'),
        ),
    ]