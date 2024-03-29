# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 19:31
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0014_auto_20160628_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='Uncheck this to remove without deleting')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last modification time')),
                ('file', models.FileField(upload_to='seminars/%Y/%m')),
                ('description', models.CharField(blank=True, max_length=250)),
                ('seminar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seminars.Seminar')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
