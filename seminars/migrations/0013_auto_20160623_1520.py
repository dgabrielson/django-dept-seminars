# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0012_auto_20160623_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]
