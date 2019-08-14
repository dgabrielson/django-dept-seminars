from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.utils.timezone import now

from seminars.models import Seminar, SeminarCancelAnnouncement


def get_queryset(startfrom_dtstart=None, upto_dtstart=None):
    weeks_in_advance = getattr(settings, 'SEMINAR_UPCOMING_WEEKS_IN_ADVANCE', 3)
    max_count = getattr(settings, 'SEMINAR_UPCOMING_MAX_COUNT', 3)
    always_days = getattr(settings, 'SEMINAR_UPCOMING_ALWAYS_DAYS', 7)

    if startfrom_dtstart is None:
        seminar_now = now()
        today = seminar_now.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        today = startfrom_dtstart

    if upto_dtstart is None:
        plusNweeks = today + datetime.timedelta(days=weeks_in_advance*7)
    else:
        plusNweeks = upto_dtstart

    plusNdays = today + datetime.timedelta(days=always_days)
    seminars = Seminar.objects.active().advertised().filter(
                                      when__range=(today,  plusNweeks)
                                      ).reverse()
    if upto_dtstart is None:
        seminars_always = seminars.filter(when__range=(today, plusNdays))
        count = max([max_count, seminars_always.count()])
        seminars = seminars[:count]

    return seminars


def upcoming_seminars(request):
    """
    Returns upcoming seminars.
    Use the configuration parameters UPCOMING_WEEKS_IN_ADVANCE and
    UPCOMING_MAX_COUNT to fine tune results.
    """
    weeks_in_advance = getattr(settings, 'SEMINAR_UPCOMING_WEEKS_IN_ADVANCE', 3)
    max_count = getattr(settings, 'SEMINAR_UPCOMING_MAX_COUNT', 3)

    seminar_now = now()
    today = seminar_now.replace(hour=0, minute=0, second=0, microsecond=0)
    plusNweeks = today + datetime.timedelta(days=weeks_in_advance*7)
    urgent_notices = SeminarCancelAnnouncement.objects.filter(
                            active=True,
                            urgent=True,
                            when__range=(today,  plusNweeks),
                        ).order_by('when')
    urgent_notices = urgent_notices[:max_count]
    seminars = get_queryset()
    return {
        'upcoming_seminars': seminars,
        'urgent_notices': urgent_notices,
    }


#
