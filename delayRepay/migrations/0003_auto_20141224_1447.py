# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0002_journey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_type', models.CharField(max_length=200)),
                ('cost', models.CharField(max_length=200)),
                ('ticket_photo_path', models.CharField(max_length=200)),
                ('ticket_start_date', models.DateField()),
                ('ticket_expire_date', models.DateField()),
                ('delayRepayUser', models.ForeignKey(to='delayRepay.UserData')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='journey',
            name='delayRepayUser',
            field=models.ForeignKey(default=None, to='delayRepay.UserData'),
            preserve_default=False,
        ),
    ]
