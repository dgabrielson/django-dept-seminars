"""
The url patterns for the seminars application.

"""
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views
from .feeds import SeminarFeed, SeminarSeriesFeed
from .models import Seminar

urlpatterns = [
    url(r'^$',
        views.archive_index,
        name='seminars-archive',
        ),
    url(r'^all-future/$',
        views.all_future,
        name='seminars-all-future',
        ),
    url(r'^(?P<year>\d{4})/$',
        views.archive_year,
        name='seminars-archive-year',
        ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.archive_month,
        name='seminars-archive-month',
        ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.archive_day,
        name='seminars-archive-day',
        ),
    url(r'^series/$',
        views.series_list,
        name='seminars-series-list',
        ),
    url(r'^series/(?P<series>[\w-]+)/$',
        views.series_archive_index,
        name='seminars-series-detail',
        ),
    url(r'^series/(?P<slug>[\w-]+)/at-a-glance/$',
        views.at_a_glance,
        name='seminars-at-a-glance',
        ),
    url(r'^series/(?P<series>[\w-]+)/(?P<year>\d{4})/$',
        views.series_archive_year,
        name='seminars-series-archive-year',
        ),
    url(r'^series/(?P<series>[\w-]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.series_archive_month,
        name='seminars-series-archive-month',
        ),
    url(r'^series/(?P<series>[\w-]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.series_archive_day,
        name='seminars-series-archive-day',
        ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$',
        views.seminar_detail,
        name='seminars-seminar-detail',
        ),
    url(r'^series/(?P<series>[\w-]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$',
        views.seminar_detail_one_series,
        name='seminars-series-seminar-detail',
        ),

    # SOCIAL
    url(r'^feed/$',
        SeminarFeed(),
        name='seminars-feed',
        ),
    url(r'^calendar.ics$',
        views.generic_queryset_icalendar,
        kwargs={'queryset': Seminar.objects.active(),},
        name='seminars-calendar',
        ),
    url(r'^calendar$', RedirectView.as_view(url='calendar.ics', permanent=True)),

    url(r'^series/(?P<series>[\w-]+)/feed/$',
        SeminarSeriesFeed(),
        name='seminars-series-feed',
        ),
    url(r'^series/(?P<series>[\w-]+)/calendar.ics$',
        views.seminarseries_icalendar,
        kwargs={'queryset': Seminar.objects.active(),},
        name='seminars-series-calendar',
        ),
    url(r'^series/(?P<series>[\w-]+)/calendar$', RedirectView.as_view(url='calendar.ics', permanent=True)),

    ]
