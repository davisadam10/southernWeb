# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0013_delay_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='delay',
            name='claimable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
