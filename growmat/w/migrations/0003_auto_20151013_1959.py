# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('w', '0002_auto_20151011_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operation', models.CharField(default=0, max_length=2, choices=[(b'<', b'<'), (b'==', b'='), (b'>', b'>'), (b'!=', b'!')])),
                ('parameter', models.IntegerField(default=0, null=True, blank=True)),
                ('ouput_parameter', models.CharField(max_length=256, null=True, blank=True)),
                ('description', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='instrument',
            name='name',
            field=models.CharField(default=b'NEW', max_length=256),
        ),
        migrations.AddField(
            model_name='rule',
            name='input',
            field=models.ForeignKey(related_name='input_instrument', to='w.Instrument'),
        ),
        migrations.AddField(
            model_name='rule',
            name='output',
            field=models.ForeignKey(related_name='output_instrument', to='w.Instrument'),
        ),
    ]
