# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import delayRepay.models


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0007_auto_20150104_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_photo',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=delayRepay.models.get_image_path),
            preserve_default=True,
        ),
    ]
