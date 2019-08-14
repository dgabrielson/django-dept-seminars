# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminar',
            name='speaker_url',
            field=models.URLField(verbose_name="Speaker's URL", blank=True),
        ),
    ]
