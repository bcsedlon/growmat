# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0005_auto_20151013_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(default=0, null=True, blank=True)),
                ('status', models.IntegerField(default=0, null=True, blank=True)),
                ('datetime', models.DateTimeField(null=True, blank=True)),
                ('instrument', models.ForeignKey(to='w.Instrument')),
            ],
        ),
    ]
