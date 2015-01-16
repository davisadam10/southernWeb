# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delayRepay', '0008_auto_20150111_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='delay',
            name='claimed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userdata',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to='delayRepay.UserData'),
            preserve_default=True,
        ),
    ]
