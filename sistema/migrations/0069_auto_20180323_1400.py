# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-03-23 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0068_existencia_fondo_fijo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devueltosaladetalle',
            name='saldo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pedidosaladetalle',
            name='saldo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
