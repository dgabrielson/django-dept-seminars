# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-31 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0017_auto_20161031_1105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seminarseries',
            options={'ordering': ['ordering', 'verbose_name'], 'verbose_name': 'series', 'verbose_name_plural': 'series'},
        ),
        migrations.AddField(
            model_name='seminarseries',
            name='ordering',
            field=models.PositiveSmallIntegerField(default=50, help_text='Use this to change the ordering of series in a list (series with the same number are sorted by title)', verbose_name='ordering'),
        ),
        migrations.AlterField(
            model_name='seminarseries',
            name='verbose_name',
            field=models.CharField(help_text='Title of this seminar series', max_length=100, verbose_name='title'),
        ),
    ]