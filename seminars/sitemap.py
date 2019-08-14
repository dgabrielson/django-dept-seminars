"""
Sitemap for seminars application
"""
from __future__ import unicode_literals

from copy import copy

from django.contrib.sitemaps import GenericSitemap

from .models import Seminar

Seminar_Sitemap = GenericSitemap({
                        'queryset': Seminar.objects.active().exclude_tba()
                    })
