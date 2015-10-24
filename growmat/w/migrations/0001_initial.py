# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0, choices=[(0, b'SYSTEM'), (80, b'OUTPUT'), (20, b'THERMOMETER'), (40, b'HUMIDITYMETER'), (60, b'DISTANCEMETER'), (80, b'PHMETER')])),
                ('index', models.IntegerField(default=0, choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9')])),
                ('name', models.CharField(default=b'Instrument', max_length=256)),
                ('value', models.IntegerField(default=0, null=True, blank=True)),
                ('status', models.IntegerField(default=0, null=True, blank=True)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
