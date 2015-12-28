# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0016_auto_20151117_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rule',
            old_name='operation',
            new_name='input_operation',
        ),
        migrations.RenameField(
            model_name='rule',
            old_name='output_parameter',
            new_name='output_parameter_false',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='action',
        ),
        migrations.AddField(
            model_name='instrument',
            name='datatype',
            field=models.IntegerField(default=0, choices=[(0, b'int'), (1, b'float')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='output_action_false',
            field=models.CharField(default=b'None', max_length=4, choices=[(b'None', b'None'), (b'=', b'='), (b'&', b'&'), (b'& ~', b'& ~'), (b'|', b'|'), (b'| ~', b'| ~'), (b'+', b'+'), (b'-', b'-'), (b'*', b'*'), (b'/', b'/'), (b'%', b'%')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='output_action_true',
            field=models.CharField(default=b'None', max_length=4, choices=[(b'None', b'None'), (b'=', b'='), (b'&', b'&'), (b'& ~', b'& ~'), (b'|', b'|'), (b'| ~', b'| ~'), (b'+', b'+'), (b'-', b'-'), (b'*', b'*'), (b'/', b'/'), (b'%', b'%')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='output_parameter_true',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='manual',
            field=models.BooleanField(default=False),
        ),
    ]
