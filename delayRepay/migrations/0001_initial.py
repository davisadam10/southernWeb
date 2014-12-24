# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('journeyName', models.CharField(max_length=200)),
                ('departingStation', models.CharField(max_length=200)),
                ('arrivingStation', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_type', models.CharField(max_length=200)),
                ('cost', models.CharField(max_length=200)),
                ('ticket_photo_path', models.CharField(max_length=200)),
                ('ticket_start_date', models.DateField()),
                ('ticket_expire_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('title', models.CharField(max_length=4)),
                ('forename', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('phoneNum', models.CharField(max_length=200)),
                ('address1', models.CharField(max_length=200)),
                ('address2', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('county', models.CharField(max_length=200)),
                ('postcode', models.CharField(max_length=7)),
                ('photocard_id', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='ticket',
            name='delayRepayUser',
            field=models.ForeignKey(to='delayRepay.UserData'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journey',
            name='delayRepayUser',
            field=models.ForeignKey(to='delayRepay.UserData'),
            preserve_default=True,
        ),
    ]
