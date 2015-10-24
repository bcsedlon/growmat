# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0010_auto_20151019_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='status',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
