# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-07-03 17:25
from __future__ import unicode_literals

import sistema.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0118_auto_20180703_1250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sala',
            options={'ordering': ['centro_costo']},
        ),
        migrations.AlterModelOptions(
            name='servicio',
            options={},
        ),
        migrations.RemoveField(
            model_name='farmacia',
            name='usuarios',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='apodo',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='centro_costo',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='nombre',
        ),
        migrations.AddField(
            model_name='farmacia',
            name='apodo',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='farmacia',
            name='centro_costo',
            field=models.CharField(default=1, max_length=3, unique=True, validators=[sistema.models.validar]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sala',
            name='apodo',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(default=1, max_length=3, unique=True, validators=[sistema.models.validar]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicio',
            name='farmacia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='farmacia', to='sistema.Farmacia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicio',
            name='sala',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sala', to='sistema.Sala'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[sistema.models.validar]),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='servicio',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='sala',
            name='servicio',
            field=models.CharField(max_length=40),
        ),
    ]
