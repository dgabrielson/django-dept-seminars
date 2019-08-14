"""
Views for the seminars application.
"""
#######################################################################
from __future__ import unicode_literals

import datetime

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic import (ArchiveIndexView, DateDetailView,
            YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView,
            DetailView, ListView, FormView,
            CreateView, DeleteView, UpdateView,
            )

from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from classes.models import Semester
from webcal.views import generic_queryset_icalendar


from .. import conf
from ..context_processors import upcoming_seminars
from ..forms import SeminarForm, BulkCreateSeminarForm
from ..models import Seminar, SeminarCancelAnnouncement, SeminarSeries

from ..mixins import SingleFKFormViewMixin, RestrictedFormViewMixin

#######################################################################
#######################################################################
#######################################################################

class SeriesMixin(object):
    model = SeminarSeries
    queryset = SeminarSeries.objects.active()

#######################################################################

class SeriesShowMixin(SeriesMixin):
    model = SeminarSeries
    queryset = SeriesMixin.queryset.show()

#######################################################################

class SeriesListView(SeriesShowMixin, ListView):
    pass

series_list = SeriesListView.as_view()

#######################################################################

class SeriesDetailView(SeriesMixin, DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super(SeriesDetailView, self).get_context_data(*args, **kwargs)
        context.update({'seminar_now': now()})
        return context

series_detail = SeriesDetailView.as_view()
at_a_glance = SeriesDetailView.as_view(template_name='seminars/at_a_glance.html')


#######################################################################
#######################################################################
#######################################################################


class SeminarMixin(object):
    """
    Core mix-in for Seminar objects
    """
    model = Seminar
    queryset = Seminar.objects.active().advertised()
    form_class = SeminarForm

    def get_context_data(self, *args, **kwargs):
        """
        Insert the upcoming seminars in case the context processor
        is not running.
        """
        context = super(SeminarMixin, self).get_context_data(*args, **kwargs)
        context.update({'seminar_now': now()})
        return context


#######################################################################

class SeminarShowMixin(SeminarMixin):
    """
    Core mix-in for Seminar objects
    """
    queryset = SeminarMixin.queryset.show()


#######################################################################

class SeminarOneSeriesMixin(SeminarMixin):
    """
    Restricted to a single seminar series.  The series slug
    must be supplied by the url pattern.
    """
    def get_series(self):
        if not hasattr(self, '_series'):
            series_slug = self.kwargs.get('series', None)
            self._series = get_object_or_404(SeminarSeries,
                                             slug=series_slug, active=True)
        return self._series


    def get_queryset(self, *args, **kwargs):
        qs = super(SeminarMixin, self).get_queryset(*args, **kwargs)
        series = self.get_series()
        return qs.filter(series=series)


    def get_context_data(self, *args, **kwargs):
        """
        Insert the upcoming seminars in case the context processor
        is not running.
        """
        context = super(SeminarOneSeriesMixin, self).get_context_data(*args, **kwargs)
        context.update({'seminarseries': self.get_series()})
        return context

#######################################################################
#######################################################################

class ArchiveMixin(object):
    """
    Mix-in for date based archives of Seminar objects
    """
    date_field = 'when'
    month_format='%m'
    allow_future = True
    allow_empty = True


#######################################################################

class SeminarArchiveIndexView(ArchiveMixin, SeminarShowMixin, ArchiveIndexView):
    """
    The main index for seminars.
    """
    def get_context_data(self, *args, **kwargs):
        """
        Insert the upcoming seminars in case the context processor
        is not running.
        """
        context = super(SeminarArchiveIndexView, self).get_context_data(
                                                            *args, **kwargs)
        context.update(upcoming_seminars(self.request))
        return context


archive_index = SeminarArchiveIndexView.as_view(allow_future=False)
all_future = SeminarArchiveIndexView.as_view(
                    queryset=SeminarArchiveIndexView.queryset.future(),
                    template_name='seminars/all_future.html')


#######################################################################

class SeminarSeriesArchiveIndexView(ArchiveMixin, SeminarOneSeriesMixin, ArchiveIndexView):
    template_name = 'seminars/seminarseries_detail.html'
series_archive_index = SeminarSeriesArchiveIndexView.as_view()

#######################################################################

class SeminarYearArchiveView(ArchiveMixin, SeminarShowMixin, YearArchiveView):
    """
    Annual archive for seminars.
    """
archive_year = SeminarYearArchiveView.as_view(make_object_list=True)


class SeminarSeriesYearArchiveView(ArchiveMixin, SeminarOneSeriesMixin, YearArchiveView):
    """
    Annual archive for seminars.
    """
series_archive_year = SeminarSeriesYearArchiveView.as_view(make_object_list=True)


#######################################################################

class SeminarMonthArchiveView(ArchiveMixin, SeminarShowMixin, MonthArchiveView):
    """
    Monthly archive for seminars.
    """
archive_month = SeminarMonthArchiveView.as_view()


class SeminarSeriesMonthArchiveView(ArchiveMixin, SeminarOneSeriesMixin, MonthArchiveView):
    """
    Monthly archive for seminars.
    """
series_archive_month = SeminarSeriesMonthArchiveView.as_view()


#######################################################################

class SeminarWeekArchiveView(ArchiveMixin, SeminarShowMixin, WeekArchiveView):
    """
    Weekly archive for seminars.
    """
archive_week = SeminarWeekArchiveView.as_view()


class SeminarSeriesWeekArchiveView(ArchiveMixin, SeminarOneSeriesMixin, WeekArchiveView):
    """
    Weekly archive for seminars.
    """
series_archive_week = SeminarSeriesWeekArchiveView.as_view()


#######################################################################

class SeminarDayArchiveView(ArchiveMixin, SeminarShowMixin, DayArchiveView):
    """
    Daily archive for seminars.
    """
archive_day = SeminarDayArchiveView.as_view()


class SeminarSeriesDayArchiveView(ArchiveMixin, SeminarOneSeriesMixin, DayArchiveView):
    """
    Daily archive for seminars.
    """
series_archive_day = SeminarSeriesDayArchiveView.as_view()


#######################################################################

class SeminarDetailView(ArchiveMixin, SeminarMixin, DateDetailView):
    """
    Details for a seminar.
    """
seminar_detail = SeminarDetailView.as_view()


class SeminarOneSeriesDetailView(ArchiveMixin, SeminarOneSeriesMixin, DateDetailView):
    """
    Details for a seminar specific to a series.
    """
seminar_detail_one_series = SeminarOneSeriesDetailView.as_view()


#######################################################################
#######################################################################

def seminarseries_icalendar(request, *args, **kwargs):
    series = kwargs.pop('series', None)
    kwargs['queryset'] = kwargs['queryset'].filter(series__slug=series)
    return generic_queryset_icalendar(request, *args, **kwargs)

#######################################################################
#######################################################################
#######################################################################
