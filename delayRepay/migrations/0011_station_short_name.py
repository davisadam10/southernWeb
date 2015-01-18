# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0010_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='short_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
