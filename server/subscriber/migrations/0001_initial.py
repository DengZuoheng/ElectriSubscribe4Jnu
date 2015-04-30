# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('what', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dorm', models.CharField(max_length=4)),
                ('feedback_type', models.CharField(default=b'mail', max_length=8)),
                ('alarm_mode', models.CharField(max_length=128)),
                ('lower_limit', models.FloatField(default=30.0, blank=True)),
                ('current_remain', models.FloatField(default=30.0, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
