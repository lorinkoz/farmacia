# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-03-26 16:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0072_auto_20180326_1230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='existencia',
            options={'ordering': ['producto']},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['unidad', 'nombre']},
        ),
        migrations.AlterOrderWithRespectTo(
            name='devueltocama',
            order_with_respect_to='cama',
        ),
        migrations.AlterOrderWithRespectTo(
            name='pedidocama',
            order_with_respect_to='cama',
        ),
    ]
