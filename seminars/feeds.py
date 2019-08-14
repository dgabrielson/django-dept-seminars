# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy

from seminars.models import Seminar, SeminarSeries


class SeminarFeed(Feed):
    title = "Seminars feed"
    link = reverse_lazy('seminars-archive')
    title_template = 'seminars/feed/title.html'
    description_template = 'seminars/feed/description.html'


    def items(self):
        weeks_in_advance = getattr(settings, 'UPCOMING_WEEKS_IN_ADVANCE', 3)
        today = datetime.date.today()
        plusNweeks = today + datetime.timedelta(days=weeks_in_advance*7)
        seminars = Seminar.objects.filter(active=True,
                                          when__range=(today,  plusNweeks),
                                          ).advertised().reverse()
        return seminars


    def item_pubdate(self, item):
        # this return value needs to be a datetime-compatible field, i.e., a models.DateTimeField
        return item.modified
        
    def item_link(self, item):
        return item.get_absolute_url() or self.link


class SeminarSeriesFeed(SeminarFeed):

    def get_object(self, request, series):
        return SeminarSeries.objects.active().get(slug=series)

    def title(self, obj):
        return obj.verbose_name
        
    def description(self, obj):
        return obj.description
        
    def link(self, obj):
        return obj.get_absolute_url() 

    def items(self, obj):
        qs = super(SeminarSeriesFeed, self).items()
        return qs.filter(series=obj)

    def item_link(self, item):
        return item.get_absolute_url() or item.series.get_absolute_url()

#
