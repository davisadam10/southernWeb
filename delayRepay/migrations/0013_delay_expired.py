# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0012_delay_journey'),
    ]

    operations = [
        migrations.AddField(
            model_name='delay',
            name='expired',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
