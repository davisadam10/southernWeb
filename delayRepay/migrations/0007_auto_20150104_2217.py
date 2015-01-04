# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0006_auto_20150104_2206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='ticket_expire_date',
            new_name='ticket_expiry_date',
        ),
    ]
