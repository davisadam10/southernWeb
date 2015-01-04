# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import delayRepay.models


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0003_auto_20150104_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_photo',
            field=models.ImageField(upload_to=delayRepay.models.get_image_path),
            preserve_default=True,
        ),
    ]
