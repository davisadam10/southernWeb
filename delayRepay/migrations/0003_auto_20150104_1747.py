# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0002_auto_20150104_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_photo_path',
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_photo',
            field=models.ImageField(default=None, upload_to=b''),
            preserve_default=False,
        ),
    ]
