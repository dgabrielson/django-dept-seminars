"""
The DEFAULT configuration is loaded when the CONFIG_NAME dictionary
is not present in your settings.

All valid application settings must have a default value.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.text import slugify

CONFIG_NAME = 'SEMINARS_CONFIG'    # must be uppercase!


#############################################################

def seminar_slugify(instance):
    if instance.slug:
        return instance.slug
    if instance.speaker and instance.title:
        return slugify("{} {}".format(instance.speaker, instance.title))
    return ''


#############################################################

def default_seminar_vevent_summary(instance):
    summary = 'Seminar - ' + instance.speaker
    if instance.title:
        summary += ' - "' + instance.title + '"'
    return summary

#############################################################

###
### advertised logic
###
def default_advertised_queryset(queryset):
    return queryset.exclude(speaker='')

def default_advertised_model(model):
    return bool(model.speaker)


###
### detail_linked logic
###
def default_detail_linked_queryset(queryset):
    from django.db.models import Q
    return queryset.active().exclude(Q(speaker='') or Q(title='') or Q(slug='') or Q(slug__isnull=True))

def default_detail_linked_model(model):
    if not (model.active and model.series.active):
        return False
    if not model.slug:
        return False
    return bool(model.speaker) and bool(model.title)

#############################################################

DEFAULT = {
    # 'storage' is the storage backend for files.
    # (optional)
    'storage':  default_storage,

    # 'upload_to' is the variable portion of the path where files are stored.
    # (optional)
    'upload_to': 'seminars/%Y/%m',

    # a callable that takes the seminar object and returns the vevent
    # summary text.
    'seminar_vevent_summary': default_seminar_vevent_summary,

    # advertised logic
    'logic:advertised': {
        'queryset': default_advertised_queryset,
        'model': default_advertised_model,
        },

    # detail_linked logic
    'logic:detail_linked': {
        'queryset': default_detail_linked_queryset,
        'model': default_detail_linked_model,
        },

    # this should *never* change after your deployment is up and running
    'location_choices_filter': {'active': True},
    'location_help': ''''If you require a location not in the list,
please contact an administrator''',

    'restructuredtext_help':  '''This will be processed as
<a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">
ReStructuredText</a>.''',

    # define where to load the form assets from:
    'location:model': 'places.ClassRoom',

    'active:help_text': 'Uncheck this to remove without deleting',

    'series:verbose_name': 'series',
    'series:verbose_name_plural': 'series',

    'series:verbose_name:verbose_name': 'title',
    'series:verbose_name:help_text': 'Title of this seminar series',

    'series:short_name:verbose_name': 'short name',
    'series:short_name:help_text': 'A short name for this seminar series (do not include the descriptor, below)',

    'series:descriptor:verbose_name': 'descriptor',
    'series:descriptor:help_text': 'A term that describes a single event in this series (such as: "lecture", "talk" or "seminar") [use lower case]',

    'series:descriptor_plural:verbose_name': 'plural descriptor',
    'series:descriptor_plural:help_text': 'A term that describes multile events in this series (plural of above)',

    'series:slug:verbose_name': 'URL fragment',
    'series:slug:help_text': 'A url fragment which uniquely identifies this seminar series',

    'series:show_seminars:verbose_name': 'show seminars in main archive',
    'series:show_seminars:help_text': 'Seminars from this series will be included in all lists and advertising (as long as the speaker is set)',
    'series:show_series:verbose_name': 'show series in series list',
    'series:show_series:help_text': 'This series will show in the list of series',

    'series:organizer:model': 'auth.Group',
    'series:organizer:verbose_name': 'organizing group',
    'series:organizer:allow_null': True,
    'series:organizer:limit_choices_to': {},
    'series:organizer:help_text': 'User group that is in charge of this seminar series (should have add, change, delete permissions for seminars)',
    'series:organizer:admin:help:title': 'Series Organizing Group Help',
    'series:organizer:admin:help:breadcrumb': 'Organizing Group Help',

    # value is day of week as reported by date.isoweekday()
    'series:default_dayofweek:choices': ((1, 'Monday'),
                                         (2, 'Tuesday'),
                                         (3, 'Wednesday'),
                                         (4, 'Thursday'),
                                         (5, 'Friday'), ),
    'series:default_dayofweek:verbose_name': 'usual day',
    'series:default_dayofweek:help_text': 'The day of the week this seminar series normally occurs',

    # value is the number of days of the recurrence.
    'series:default_interval:choices': ((0, 'Irregular'),
                                        (7, 'Every week'),
                                        (14, 'Every 2 weeks'),
                                        (21, 'Every 3 weeks'),
                                        ),
    'series:default_interval:verbose_name': 'usual occurance',
    'series:default_interval:help_text': 'The seminar series normally occurs this often',

    'series:default_time:verbose_name': 'usual time',
    'series:default_time:help_text': 'The usual time seminars begin (use 24-hour time)',

    'series:default_location:verbose_name': 'usual location',
    'series:default_location:help_text': 'The usual location for this seminars series',

    'series:default_duration:default_value': 60,
    'series:default_duration:help_text': 'The usual number of <strong>minutes</strong> a seminar runs for',
    'series:default_duration:verbose_name': 'usual duration',

    'series:ordering:verbose_name': 'ordering',
    'series:ordering:help_text': 'Use this to change the ordering of series in a list (series with the same number are sorted by title)',

    'seminar:series:verbose_name': 'seminar series',
    'seminar:series:help_text': 'Which seminar series this belongs to',
    'seminar:speaker:verbose_name': 'speaker',
    'seminar:speaker:help_text': 'Who is giving the talk',
    'seminar:speaker_url:verbose_name': "speaker's url",
    'seminar:speaker_url:help_text': "An optional link to the speaker's website",
    'seminar:affiliation:verbose_name': "affiliation",
    'seminar:affiliation:help_text': "The speaker's home institution or department (recommended)",
    'seminar:when:verbose_name': 'date and time',
    'seminar:when:help_text': 'When the seminar begins',
    'seminar:duration:verbose_name': 'duration',
    'seminar:duration:help_text': 'How long this seminar runs for, in <strong>minutes</strong> (leave blank for default)',
    'seminar:title:verbose_name': 'title',
    'seminar:title:help_text': 'The title of the talk',
    'seminar:slug:verbose_name': 'URL fragment',
    'seminar:slug:populate_from': seminar_slugify,
    'seminar:slug:help_text': 'A url fragment which uniquely identifies this seminar',
    'seminar:slug:validation_error':  "This url fragment already exists for this date",
    'seminar:abstract_url:verbose_name': 'abstract url',
    'seminar:abstract_url:help_text': 'An optional link to the talk abstract',
    'seminar:abstract:verbose_name': 'abstract',
    'seminar:abstract:help_text': '''The text of  abstract. This will be processed as
<a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">
ReStructuredText</a>.''',
    'seminar:note:verbose_name': 'note',
    'seminar:note:help_text': 'An optional additional note for advertising (e.g., coffee)',



    'user_is_admin_restricted': lambda instance, user: user.groups.filter(seminarseries__isnull=False).exists(),
    'series:user_filter': 'organizer__user',
    'series:restricted_fields': ['organizer', 'slug', 'ordering', ],
    'series:restricted_extra_filters': {'active': True, },
    'seminar:user_filter': 'series__organizer__user',
    'seminar:restricted_fields': [],
    'seminar:restricted_extra_filters': {'active': True, 'series__active': True, },
}





def get(setting):
    """
    get(setting) -> value

    setting should be a string representing the application settings to
    retrieve.
    """
    assert setting in DEFAULT, 'the setting %r has no default value' % setting
    app_settings = getattr(settings, CONFIG_NAME, DEFAULT)
    return app_settings.get(setting, DEFAULT[setting])


def get_all():
    """
    Return all current settings as a dictionary.
    """
    app_settings = getattr(settings, CONFIG_NAME, DEFAULT)
    return dict([(setting, app_settings.get(setting, DEFAULT[setting])) \
                 for setting in DEFAULT])
