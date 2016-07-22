# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0016_auto_20160711_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='delay',
            name='delay_details',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
