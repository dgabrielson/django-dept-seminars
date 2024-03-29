# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 20:52
from __future__ import unicode_literals

from django.db import migrations


def fix_created(apps, schema_editor):
    # We can't import the  model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    
    for model in [apps.get_model("seminars", "Seminar"),
                  apps.get_model("seminars", "SeminarCancelAnnouncement"),
                  ]:
        for obj in model.objects.all():
            obj.created = obj.modified
            obj.save()


def unfix_created(apps, schema_editor):
    pass
    


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0004_auto_20160621_1549'),
    ]

    operations = [
        migrations.RunPython(fix_created, unfix_created),
    ]
