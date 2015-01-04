# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0005_auto_20150104_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_photo',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'ticket_photos/'),
            preserve_default=True,
        ),
    ]
