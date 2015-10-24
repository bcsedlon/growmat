# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0011_auto_20151019_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'NEW', max_length=256)),
                ('time_from', models.TimeField()),
                ('time_to', models.TimeField()),
                ('description', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='rule',
            name='action',
            field=models.CharField(default=0, max_length=3, choices=[(b'=', b'='), (b'&', b'AND'), (b'|', b'OR')]),
        ),
        migrations.AddField(
            model_name='rule',
            name='period',
            field=models.ForeignKey(default=0, to='w.Period'),
            preserve_default=False,
        ),
    ]
