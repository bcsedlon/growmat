# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0008_auto_20151018_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='value',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='input_attribute',
            field=models.CharField(default=0, max_length=6, choices=[(b'VALUE', b'VALUE'), (b'STATUS', b'STATUS'), (b'NT', b'NT'), (b'IV', b'IV'), (b'W', b'WARNING'), (b'A', b'ALARM')]),
        ),
        migrations.AlterField(
            model_name='rule',
            name='output_attribute',
            field=models.CharField(default=0, max_length=6, choices=[(b'VALUE', b'VALUE'), (b'STATUS', b'STATUS'), (b'NT', b'NT'), (b'IV', b'IV'), (b'W', b'WARNING'), (b'A', b'ALARM')]),
        ),
    ]
