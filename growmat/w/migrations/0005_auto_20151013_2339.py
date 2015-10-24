# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0004_auto_20151013_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='action',
            field=models.CharField(default=0, max_length=3, choices=[(b'OFF', b'OFF'), (b'ON', b'ON')]),
        ),
    ]
