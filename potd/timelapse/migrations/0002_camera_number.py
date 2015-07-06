# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timelapse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='number',
            field=models.CharField(max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
    ]
