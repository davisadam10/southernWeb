# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0015_auto_20150423_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticketNumPart1',
            field=models.CharField(default=b'00000', max_length=200),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticketNumPart2',
            field=models.CharField(default=b'00000', max_length=200),
        ),
    ]
