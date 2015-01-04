# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('delay', models.CharField(max_length=200)),
                ('delay_reason', models.CharField(max_length=200)),
                ('delayRepayUser', models.ForeignKey(to='delayRepay.UserData')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='journey',
            name='date',
        ),
        migrations.RemoveField(
            model_name='journey',
            name='endTime',
        ),
        migrations.RemoveField(
            model_name='journey',
            name='startTime',
        ),
    ]
