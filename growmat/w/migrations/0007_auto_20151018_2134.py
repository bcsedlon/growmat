# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0006_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='status',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='value',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
    ]
