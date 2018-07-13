# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-03-23 17:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema_Gestion_Medicamentos', '0066_auto_20180323_1321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cama',
            options={'ordering': ['num_cama']},
        ),
        migrations.AlterModelOptions(
            name='existencia',
            options={'ordering': ['producto']},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['unidad', 'nombre']},
        ),
        migrations.AlterModelOptions(
            name='sala',
            options={'ordering': ['centro_costo']},
        ),
    ]
