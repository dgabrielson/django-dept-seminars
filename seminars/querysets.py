"""
Seminar querysets
"""
###############################################################
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now

from webcal.utils import make_icalendar

from . import conf

###############################################################
###############################################################
###############################################################

class CustomQuerySet(models.query.QuerySet):
    """
    Custom QuerySet.
    """
    def active(self):
        """
        Returns only the active items in this queryset
        """
        return self.filter(active=True)


###############################################################
###############################################################

class SeminarSeriesQuerySet(CustomQuerySet):
    """
    QuerySet for Seminar series.
    """
    def show(self):
        return self.filter(show_series=True)

###############################################################

class SeminarQuerySet(CustomQuerySet):
    """
    QuerySet api extensions for Seminar objects
    """
    def active(self):
        qs = super(SeminarQuerySet, self).active()
        return qs.filter(series__active=True)


    def show(self):
        return self.filter(series__show_seminars=True)


    def icalendar(self):
        return make_icalendar(self)


    def advertised(self):
        """
        Filter the queryset so only advertised seminars appear
        """
        return conf.get('logic:advertised').get('queryset')(self)


    def detail_linked(self):
        """
        Filter the queryset so only seminars with detail pages appear
        """
        return conf.get('logic:detail_linked').get('queryset')(self)


    def future(self):
        """
        Return all future seminars, including ones from now.
        """
        return self.filter(when__gte=now())


    def past(self):
        """
        Return all past seminars, including ones from now.
        """
        return self.filter(when__lte=now())


    def between_dates(self, dtstart, dtend, tzinfo=None):
        """
        Here we need to be careful, since 'dates' implies a 'date'
        object, but 'when' is a datetime object.
        When USE_TZ is True, and there is no *pre-existing*
        tzinfo on dtstart and dtend, then fix it up
        using either the supplied tzinfo, if any, or the
        default timezone for the system.
        """
        if isinstance(dtstart, datetime.date):
            dtstart = datetime.datetime(dtstart.year, dtstart.month, dtstart.day)
        if isinstance(dtend, datetime.date):
            dtend = datetime.datetime(dtend.year, dtend.month, dtend.day)
        if USE_TZ:
            if tzinfo is None:
                tzinfo = get_default_timezone()
            dtstart = make_aware(dtstart, tzinfo)
            dtend = make_aware(dtend, tzinfo)
        return self.filter(when__range=[dtstart, dtend])


    def exclude_tba(self):
        return self.exclude(title__icontains='tba')


###############################################################

class SeminarCancelAnnouncementQuerySet(CustomQuerySet):
    """
    QuerySet api extensions for SeminarCancelAnnouncementQuerySet objects
    """
    def icalendar(self):
        return make_icalendar(self)


    def future(self):
        """
        Return all future seminars, including ones from now.
        """
        return self.filter(when__gte=now)


    def past(self):
        """
        Return all past seminars, including ones from now.
        """
        return self.filter(when__lte=now)


    def between_dates(self, dtstart, dtend):
        return self.filter(when__range=[dtstart, dtend])


    def urgent(self):
        return self.filter(urgent=True)


###############################################################
###############################################################
