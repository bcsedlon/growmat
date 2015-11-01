# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0013_auto_20151024_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='action',
            field=models.CharField(default=0, max_length=3, choices=[(b'=', b'='), (b'&', b'AND'), (b'|', b'OR'), (b'+', b'+'), (b'-', b'-')]),
        ),
        migrations.AlterField(
            model_name='rule',
            name='operation',
            field=models.CharField(default=0, max_length=2, choices=[(b'<', b'<'), (b'<=', b'<='), (b'==', b'=='), (b'>', b'>'), (b'>=', b'>='), (b'!=', b'!='), (b'&', b'AND'), (b'|', b'OR')]),
        ),
    ]
