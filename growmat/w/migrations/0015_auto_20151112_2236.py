# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0014_auto_20151030_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='priority',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rule',
            name='action',
            field=models.CharField(default=0, max_length=3, choices=[(b'=', b'='), (b'&', b'AND'), (b'|', b'OR'), (b'+', b'+'), (b'-', b'-'), (b'*', b'*'), (b'/', b'/'), (b'%', b'%')]),
        ),
        migrations.AlterField(
            model_name='rule',
            name='operation',
            field=models.CharField(default=0, max_length=2, choices=[(b'<', b'<'), (b'<=', b'<='), (b'==', b'=='), (b'>', b'>'), (b'>=', b'>='), (b'!=', b'!='), (b'&', b'&'), (b'|', b'|')]),
        ),
    ]
