# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0012_auto_20151019_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
