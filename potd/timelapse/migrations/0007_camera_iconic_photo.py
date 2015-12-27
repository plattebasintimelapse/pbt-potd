# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0006_auto_20150818_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='iconic_photo',
            field=models.ImageField(null=True, upload_to=b'iconicphotos/', blank=True),
            preserve_default=True,
        ),
    ]
