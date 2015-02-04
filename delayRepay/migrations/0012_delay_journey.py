# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0011_station_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='delay',
            name='journey',
            field=models.ForeignKey(default=1, to='delayRepay.Journey'),
            preserve_default=False,
        ),
    ]
