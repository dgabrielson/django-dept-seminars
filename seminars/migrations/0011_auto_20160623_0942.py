# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0010_auto_20160623_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='slug',
            field=models.SlugField(max_length=200, unique_for_date='when'),
        ),
    ]
