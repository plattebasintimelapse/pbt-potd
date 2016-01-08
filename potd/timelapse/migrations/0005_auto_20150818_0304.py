# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0004_auto_20150709_2002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='name_slug',
            new_name='slug',
        ),
    ]
