# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0007_auto_20151018_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='parameter',
        ),
        migrations.AddField(
            model_name='rule',
            name='input_attribute',
            field=models.CharField(default=0, max_length=6, choices=[(b'VALUE', b'VALUE'), (b'STATUS', b'STATUS'), (b'NT', b'NT'), (b'IV', b'IV'), (b'W', b'W'), (b'A', b'W')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='input_parameter',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='rule',
            name='output_attribute',
            field=models.CharField(default=0, max_length=6, choices=[(b'VALUE', b'VALUE'), (b'STATUS', b'STATUS'), (b'NT', b'NT'), (b'IV', b'IV'), (b'W', b'W'), (b'A', b'W')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='output_parameter',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='action',
            field=models.CharField(default=0, max_length=3, choices=[(b'SET', b'SET')]),
        ),
        migrations.AlterField(
            model_name='rule',
            name='operation',
            field=models.CharField(default=0, max_length=2, choices=[(b'<', b'<'), (b'=', b'='), (b'>', b'>'), (b'!=', b'!='), (b'&', b'AND'), (b'|', b'OR')]),
        ),
    ]
