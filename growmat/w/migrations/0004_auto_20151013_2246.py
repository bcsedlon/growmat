# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0003_auto_20151013_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='ouput_parameter',
        ),
        migrations.AddField(
            model_name='rule',
            name='action',
            field=models.CharField(default=0, max_length=3, choices=[(b'<', b'<'), (b'==', b'='), (b'>', b'>'), (b'!=', b'<>')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rule',
            name='result',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rule',
            name='result0',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rule',
            name='operation',
            field=models.CharField(default=0, max_length=2, choices=[(b'<', b'<'), (b'==', b'='), (b'>', b'>'), (b'!=', b'<>')]),
        ),
    ]
