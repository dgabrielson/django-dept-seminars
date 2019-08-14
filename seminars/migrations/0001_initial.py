# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('speaker', models.CharField(max_length=100)),
                ('affiliation', models.CharField(max_length=150)),
                ('when', models.DateTimeField()),
                ('title', models.CharField(help_text='Use "TBA" if the title is unknown.', max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('abstract_url', models.URLField(blank=True)),
                ('abstract', models.TextField(help_text='This will be processed as\n<a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">\nReStructuredText</a>.', blank=True)),
                ('note', models.CharField(max_length=200, blank=True)),
                ('location', models.ForeignKey(on_delete=models.deletion.CASCADE, help_text='If you require a location not in the list,\nplease contact <a href="mailto:www@stats.umanitoba.ca">Dave Gabrielson</a>', to='places.ClassRoom')),
            ],
            options={
                'ordering': ['-when'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeminarCancelAnnouncement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=150)),
                ('when', models.DateField()),
                ('urgent', models.BooleanField(default=False, help_text='Urgent announcements are posted in more locations than just the at-a-glance page.')),
            ],
            options={
                'ordering': ['-when'],
            },
            bases=(models.Model,),
        ),
    ]
