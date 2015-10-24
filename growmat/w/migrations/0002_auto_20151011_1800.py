# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='type',
            field=models.IntegerField(default=0, choices=[(0, b'SYSTEM'), (10, b'OUTPUT'), (20, b'THERMOMETER'), (30, b'HUMIDITYMETER'), (40, b'DISTANCEMETER'), (50, b'PHMETER')]),
        ),
    ]
