# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-15 15:48
from __future__ import unicode_literals

import sistema.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0107_auto_20180515_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=10)),
                ('clave', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=15)),
                ('apellidos', models.CharField(max_length=40)),
            ],
        ),
        migrations.AlterField(
            model_name='cama',
            name='historia_clinica',
            field=models.CharField(max_length=11, unique=True, validators=[sistema.models.validar]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='centro_costo',
            field=models.CharField(max_length=3, unique=True, validators=[sistema.models.validar]),
        ),
    ]
