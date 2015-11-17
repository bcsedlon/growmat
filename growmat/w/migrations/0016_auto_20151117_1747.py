# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0015_auto_20151112_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='manual',
            field=models.BooleanField(default=False, choices=[(False, b'AUTO'), (True, b'MANUAL')]),
        ),
        migrations.AddField(
            model_name='instrument',
            name='priority',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='action',
            field=models.CharField(default=0, max_length=3, choices=[(b'=', b'='), (b'&', b'&'), (b'& ~', b'& ~'), (b'|', b'|'), (b'| ~', b'| ~'), (b'+', b'+'), (b'-', b'-'), (b'*', b'*'), (b'/', b'/'), (b'%', b'%')]),
        ),
        migrations.AlterField(
            model_name='rule',
            name='operation',
            field=models.CharField(default=0, max_length=2, choices=[(b'<', b'<'), (b'<=', b'<='), (b'==', b'=='), (b'>', b'>'), (b'>=', b'>='), (b'!=', b'!='), (b'and', b'AND'), (b'or', b'OR')]),
        ),
    ]
