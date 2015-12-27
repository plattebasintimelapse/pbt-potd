# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0005_auto_20150818_0304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='slug',
            new_name='camera_slug',
        ),
    ]
