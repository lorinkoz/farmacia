# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-04-11 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0078_auto_20180408_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='cama',
            name='fecha_hora',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
