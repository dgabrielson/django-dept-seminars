"""
Seminar application models
"""
###############################################################
from __future__ import unicode_literals

import datetime
import os

import vobject
from autoslug.fields import AutoSlugField
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from webcal.utils import make_icalendar

from . import conf
from .querysets import (SeminarCancelAnnouncementQuerySet, SeminarQuerySet,
                        SeminarSeriesQuerySet)

###############################################################
###############################################################
###############################################################

class SeminarsBaseModel(models.Model):
    """
    An abstract base class.
    """
    active = models.BooleanField(default=True,
                                 help_text=conf.get('active:help_text'))
    created = models.DateTimeField(auto_now_add=True, editable=False,
                                   verbose_name='creation time')
    modified = models.DateTimeField(auto_now=True, editable=False,
                                    verbose_name='last modification time')


    class Meta:
        abstract = True

###############################################################

@python_2_unicode_compatible
class SeminarSeries(SeminarsBaseModel):
    """
    Seminar series
    """
    verbose_name = models.CharField(max_length=100,
                            verbose_name=conf.get('series:verbose_name:verbose_name'),
                            help_text=conf.get('series:verbose_name:help_text'))
    short_name = models.CharField(max_length=100,
                            verbose_name=conf.get('series:short_name:verbose_name'),
                            help_text=conf.get('series:short_name:help_text'))
    descriptor = models.CharField(max_length=32,
                            verbose_name=conf.get('series:descriptor:verbose_name'),
                            help_text=conf.get('series:descriptor:help_text'))
    descriptor_plural = models.CharField(max_length=32,
                            verbose_name=conf.get('series:descriptor_plural:verbose_name'),
                            help_text=conf.get('series:descriptor_plural:help_text'))
    slug = AutoSlugField(unique=True, max_length=100,
                            populate_from='short_name',
                            verbose_name=conf.get('series:slug:verbose_name'),
                            help_text=conf.get('series:slug:help_text'))
    show_seminars = models.BooleanField(default=True,
                            verbose_name=conf.get('series:show_seminars:verbose_name'),
                            help_text=conf.get('series:show_seminars:help_text'))
    show_series = models.BooleanField(default=True,
                            verbose_name=conf.get('series:show_series:verbose_name'),
                            help_text=conf.get('series:show_series:help_text'))
    organizer = models.ForeignKey(conf.get('series:organizer:model'),
                            on_delete=models.PROTECT,
                            limit_choices_to=conf.get('series:organizer:limit_choices_to'),
                            help_text=conf.get('series:organizer:help_text'),
                            verbose_name=conf.get('series:organizer:verbose_name'),
                            null=conf.get('series:organizer:allow_null'),
                            blank=conf.get('series:organizer:allow_null'))
    default_dayofweek = models.PositiveSmallIntegerField(
                            choices=conf.get('series:default_dayofweek:choices'),
                            help_text=conf.get('series:default_dayofweek:help_text'),
                            verbose_name=conf.get('series:default_dayofweek:verbose_name'))
    default_interval = models.PositiveSmallIntegerField(
                            choices=conf.get('series:default_interval:choices'),
                            help_text=conf.get('series:default_interval:help_text'),
                            verbose_name=conf.get('series:default_interval:verbose_name'))
    default_time = models.TimeField(
                            help_text=conf.get('series:default_time:help_text'),
                            verbose_name=conf.get('series:default_time:verbose_name'))
    default_location = models.ForeignKey(conf.get('location:model'),
                            on_delete=models.PROTECT,
                            help_text=conf.get('series:default_location:help_text'),
                            verbose_name=conf.get('series:default_location:verbose_name'))
    default_duration = models.PositiveSmallIntegerField(
                            default=conf.get('series:default_duration:default_value'),
                            help_text=conf.get('series:default_duration:help_text'),
                            verbose_name=conf.get('series:default_duration:verbose_name')
                            )
    description = models.TextField(blank=True,
                            help_text=conf.get('restructuredtext_help'))
    ordering = models.PositiveSmallIntegerField(default=50,
                            help_text=conf.get('series:ordering:help_text'),
                            verbose_name=conf.get('series:ordering:verbose_name'))


    objects = SeminarSeriesQuerySet.as_manager()


    class Meta:
        ordering = ['ordering', 'verbose_name', ]
        verbose_name = conf.get('series:verbose_name')
        verbose_name_plural = conf.get('series:verbose_name_plural')


    def __str__(self):
        return self.verbose_name


    def get_absolute_url(self):
        return reverse_lazy('seminars-series-detail', kwargs={'series': self.slug, })


###############################################################

@python_2_unicode_compatible
class Seminar(SeminarsBaseModel):
    """
    Seminar objects.

    Seminar objects by default are ordered most-recent-first.
    To get oldest-first ordering, call reverse on query set.
    """
    series = models.ForeignKey(SeminarSeries, on_delete=models.PROTECT,
                        verbose_name=conf.get('seminar:series:verbose_name'),
                        help_text=conf.get('seminar:series:help_text'),
                        limit_choices_to={'active': True})
    speaker = models.CharField(max_length=100, blank=True,
                        verbose_name=conf.get('seminar:speaker:verbose_name'),
                        help_text=conf.get('seminar:speaker:help_text'))
    speaker_url = models.URLField(blank=True,
                        verbose_name=conf.get('seminar:speaker_url:verbose_name'),
                        help_text=conf.get('seminar:speaker_url:help_text'))
    affiliation = models.CharField(max_length=250, blank=True,
                        verbose_name=conf.get('seminar:affiliation:verbose_name'),
                        help_text=conf.get('seminar:affiliation:help_text'))
    when = models.DateTimeField(
                        verbose_name=conf.get('seminar:when:verbose_name'),
                        help_text=conf.get('seminar:when:help_text'))
    duration = models.PositiveSmallIntegerField(
                        blank=True, null=True,
                        verbose_name=conf.get('seminar:duration:verbose_name'),
                        help_text=conf.get('seminar:duration:help_text'))
    location = models.ForeignKey(conf.get('location:model'),
                        on_delete=models.PROTECT,
                        limit_choices_to=conf.get('location_choices_filter'),
                        help_text=conf.get('location_help'))
    title = models.CharField(max_length=200, blank=True,
                        verbose_name=conf.get('seminar:title:verbose_name'),
                        help_text=conf.get('seminar:title:help_text'))
    slug = AutoSlugField(max_length=200, blank=True, unique_with='when',
                        always_update=True,
                        populate_from=conf.get('seminar:slug:populate_from'),
                        verbose_name=conf.get('seminar:slug:verbose_name'),
                        help_text=conf.get('seminar:slug:help_text'))
    abstract_url = models.URLField(blank=True,
                        verbose_name=conf.get('seminar:abstract_url:verbose_name'),
                        help_text=conf.get('seminar:abstract_url:help_text'))
    abstract = models.TextField(blank=True,
                        verbose_name=conf.get('seminar:abstract:verbose_name'),
                        help_text=conf.get('seminar:abstract:help_text'))
    note = models.CharField(max_length=200, blank=True,
                        verbose_name=conf.get('seminar:note:verbose_name'),
                        help_text=conf.get('seminar:note:help_text'))


    objects = SeminarQuerySet.as_manager()


    class Meta:
        ordering = ['-when', ]


    def when_date_localtime(self):
        """
        Convert the seminar start datetime to a date in the local time zone.
        """
        result = self.when
        # Mimic code in django/views/generic/dates.py
        if settings.USE_TZ:
            result = timezone.localtime(result)
        return result.date()


    def get_absolute_url(self):
        """
        See https://docs.djangoproject.com/en/dev/ref/class-based-views/mixins-date-based/#datemixin
        - convert when to localtime
        """
        if self.is_detail_linked():
            # required for DateDetailView:
            when = self.when_date_localtime()
            return reverse_lazy('seminars-seminar-detail', kwargs={
                        'year': when.year, 'month': when.month, 'day': when.day,
                        'slug': self.slug, })


    def __str__(self):
        if self.speaker and self.title:
            return self.speaker + ' - ' + self.title
        if self.speaker:
            return self.speaker + ' - TBA'
        return 'TBA'


    def clean(self):
        """
        Only called by model forms -- not by save()
        """
        super(Seminar, self).clean()
        if self.slug:
            # This code mimics the ``_perform_date_checks()`` function
            #   defined in ``django.db.models.base``.
            date = self.when.date()
            lookup_kwargs = {}
            lookup_kwargs['when__day'] = date.day
            lookup_kwargs['when__month'] = date.month
            lookup_kwargs['when__year'] = date.year
            lookup_kwargs['slug'] = self.slug
            #lookup_kwargs['series'] = self.series

            qs = Seminar._default_manager.filter(**lookup_kwargs)
            # Exclude the current object from the query if we are editing an
            # instance (as opposed to creating a new one)
            if not self._state.adding and self.pk is not None:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError({"slug": conf.get('seminar:slug:validation_error')})


    def is_advertised(self):
        """
        Returns True if this is part of the advertised() queryset,
        False otherwise.
        Ensure this function uses the same logic as the queryset!
        """
        return conf.get('logic:advertised').get('model')(self)


    def is_detail_linked(self):
        """
        Returns True if this is part of the detail_linked() queryset,
        False otherwise.
        Ensure this function uses the same logic as the queryset!
        """
        return conf.get('logic:detail_linked').get('model')(self)


    def is_future(self):
        """
        Returns True if the seminar is schedule for the future; otherwise False
        Ensure this function uses the same logic as the queryset!
        """
        return self.when >= timezone.now()


    def get_duration_minutes(self):
        return self.duration or self.series.default_duration


    def icalendar(self):
        """
        http://en.wikipedia.org/wiki/ICalendar
        http://tools.ietf.org/html/rfc5545
        """
        cal = vobject.iCalendar()
        ev = self.vevent()
        if ev is not None:
            cal.add(ev)
        cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
        return cal


    def vevent(self):
        if not self.active:
            return None

        duration = datetime.timedelta(minutes=self.get_duration_minutes())

        cal = vobject.iCalendar()
        ev = cal.add('vevent')

        ev.add('dtstamp').value = self.when
        ev.add('dtstart').value = self.when
        ev.add('dtend').value = self.when + duration
        ev.add('location').value = "{}".format(self.location)
        ev.add('summary').value = conf.get('seminar_vevent_summary')(self)

        if self.is_detail_linked():
            current_site = Site.objects.get_current()
            ev.add('url').value = 'http://' + current_site.domain + \
                                        "{}".format(self.get_absolute_url())

        return ev


    def twitter_dtlist(self):
        """
        Return a list of suggested datetimes for tweeting this information.
        """
        if timezone.now() > self.when:
            # Don't tweet about things which have already started.
            return []
        return [self.when - datetime.timedelta(days=1),
                self.when - datetime.timedelta(days=7),
                ]


###############################################################

@python_2_unicode_compatible
class SeminarCancelAnnouncement(SeminarsBaseModel):
    """
    This model is a placeholder in the at-a-glance view for weeks that
    have no seminar.

    Events here are not shown in *any* of the seminar lists, other than
    at-a-glance.

    Examples messages would be:

    * No seminar
    * TA orientation
    * Rememberance day

    Or other reasons for *not* having a seminar.
    """
    message = models.CharField(max_length=150)
    when = models.DateField()
    urgent = models.BooleanField(default=False,
                                 help_text='Urgent announcements are posted ' +
                                           'in more locations than just the ' +
                                           'at-a-glance page.')


    objects = SeminarCancelAnnouncementQuerySet.as_manager()


    class Meta:
        ordering = ['-when', ]


    def __str__(self):
        return self.message


###############################################################


@python_2_unicode_compatible
class Asset(SeminarsBaseModel):
    """
    A file asset for a shout.
    """
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE,
                                limit_choices_to={'active': True})
    file = models.FileField(upload_to=conf.get('upload_to'),
                            storage=conf.get('storage'))
    description = models.CharField(max_length=250, blank=True)


    def get_absolute_url(self):
        return self.file.url
    get_absolute_url.short_description = 'url'


    def __str__(self):
        name = os.path.basename(self.file.name)
        if self.description:
            name += ': ' + self.description
        return name


###############################################################
###############################################################
###############################################################
