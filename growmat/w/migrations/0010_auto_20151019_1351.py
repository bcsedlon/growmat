# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0009_auto_20151018_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
