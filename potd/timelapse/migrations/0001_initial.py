# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('name_slug', models.SlugField()),
                ('location_x', models.FloatField()),
                ('location_y', models.FloatField()),
                ('description', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'photos/')),
                ('photo_description', models.TextField(null=True, blank=True)),
                ('photo_datetime', models.DateTimeField()),
                ('photo_aperture', models.CharField(max_length=50)),
                ('photo_shutter_speed', models.CharField(max_length=50)),
                ('photo_iso', models.CharField(max_length=50)),
                ('camera', models.ForeignKey(to='timelapse.Camera')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeLapse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movie', models.FileField(upload_to=b'movies/')),
                ('movie_date', models.DateTimeField()),
                ('movie_description', models.TextField(null=True, blank=True)),
                ('camera', models.ForeignKey(to='timelapse.Camera')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
