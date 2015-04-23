# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0014_delay_claimable'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userdata',
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
