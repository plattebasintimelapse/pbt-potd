# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0002_camera_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
