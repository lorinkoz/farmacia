# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-17 04:30
from __future__ import unicode_literals

import Sistema_Gestion_Medicamentos.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Sistema_Gestion_Medicamentos', '0111_auto_20180516_2324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permisoglobal',
            name='farmacia_jefe_farmacia',
        ),
        migrations.RemoveField(
            model_name='permisoglobal',
            name='jefe_farmacia_contabilidad',
        ),
        migrations.AddField(
            model_name='permisoglobal',
            name='farmacia',
            field=models.ManyToManyField(blank=True, related_name='farmacia', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='permisoglobal',
            name='jefe_contabilidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jefe_contabilidad', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
        migrations.RemoveField(
            model_name='permisoglobal',
            name='contabilidad',
        ),
        migrations.AddField(
            model_name='permisoglobal',
            name='contabilidad',
            field=models.ManyToManyField(blank=True, related_name='contabilidad', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[Sistema_Gestion_Medicamentos.models.validar]),
        ),
    ]