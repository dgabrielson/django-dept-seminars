##########################################################################
from __future__ import unicode_literals

from datetime import date, datetime

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from . import conf
from .admin_utils import UsedValuesForeignKeyFilter
from .forms import AdminSeminarForm, AdminSeminarSeriesForm
from .mixins import (ClassBasedViewsAdminMixin, RestrictedAdminMixin,
                     SingleFKAdminMixin)
from .models import Asset, Seminar, SeminarCancelAnnouncement, SeminarSeries
from .views.admin import (BulkCreateSeminarAdminView,
                          SeminarSeriesOrganizerHelpAdminView)

##########################################################################

class SeminarSeriesFilter(UsedValuesForeignKeyFilter):
    title = 'seminar series'
    parameter_name = 'series__id__exact'
    field_name = 'series'
    allow_none = False
    model = SeminarSeries


##########################################################################

class SeminarSeriesAdmin(RestrictedAdminMixin, ClassBasedViewsAdminMixin,
                         admin.ModelAdmin):
    form = AdminSeminarSeriesForm
    list_display = ['verbose_name', 'active', 'organizer', ]
    list_filter = ['active', ]
    is_restricted_user = conf.get('user_is_admin_restricted')
    restricted_user_filter = conf.get('series:user_filter')
    restricted_exclude_fields = conf.get('series:restricted_fields')
    restricted_extra_filters = conf.get('series:restricted_extra_filters')


    def get_urls(self):
        """
        Add in the bulk create option
        """
        urls = super(SeminarSeriesAdmin, self).get_urls()
        urls = [url(r'^organizer/help/$',
                    self.admin_site.admin_view(
                        permission_required('seminars.change_seminarseries')(
                        self.cb_changeform_view)),
                    kwargs={'view_class': SeminarSeriesOrganizerHelpAdminView,
                            'title': conf.get('series:organizer:admin:help:title'),
                            'add': False,
                            'original': conf.get('series:organizer:admin:help:breadcrumb'),
                            },
                    name='seminars_seminarseries_organizer_help',
                    ),
                ] + urls
        return  urls


    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Modify foreign key querysets to also be resticted.
        """
        field = super(SeminarSeriesAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'organizer':
            field.help_text += ' <a href="{0}">(help)</a>'.format(
                    reverse_lazy('admin:seminars_seminarseries_organizer_help'))
        return field


admin.site.register(SeminarSeries, SeminarSeriesAdmin)


##########################################################################

class AssetInline(admin.TabularInline):
    model = Asset
    fields = ['file', 'description', 'get_absolute_url', ]
    readonly_fields = ['get_absolute_url', ]
    extra = 0

###############################################################

class SeminarAdmin(SingleFKAdminMixin, RestrictedAdminMixin,
                   ClassBasedViewsAdminMixin, admin.ModelAdmin):
    date_hierarchy = 'when'
    inlines = [AssetInline, ]
    list_display = ['__str__', 'when', ]
    list_filter = ['when', SeminarSeriesFilter,  'modified', ]
    search_fields = ['speaker', 'title', ]
    ordering = ['-when', ]
    form = AdminSeminarForm
    fieldsets = ((None, {'fields': (('series', 'active', ), ), }),
                 ('Speaker',
                    {'fields': ('speaker', 'speaker_url', 'affiliation'), }),
                 ('Title and abstract',
                    {'fields': ('title', 'abstract_url', 'abstract', 'note'), }),
                 ('Date, time, and place',
                    {'fields': (('when', 'duration', ), 'location'), }),
                 )
    save_on_top = True

    # RestrictedAdminMixin
    is_restricted_user = conf.get('user_is_admin_restricted')
    restricted_user_filter = conf.get('seminar:user_filter')
    restricted_exclude_fields = conf.get('seminar:restricted_fields')
    restricted_foreign_key_fields = {'series': conf.get('series:user_filter')}
    restricted_extra_filters = conf.get('seminar:restricted_extra_filters')

    # SingleFKAdminMixin
    single_fk_src = 'series'
    single_fk_initial = {'location': 'default_location',
                         'when': lambda series: make_aware(datetime.combine(date.today(), series.default_time)),
                         }


    def get_urls(self):
        """
        Add in the bulk create option
        """
        urls = super(SeminarAdmin, self).get_urls()
        urls = [url(r'^bulk-create/$',
                    self.admin_site.admin_view(
                        permission_required('seminars.add_seminar')(
                        self.cb_changeform_view)),
                    kwargs={'view_class': BulkCreateSeminarAdminView, },
                    name='seminars_seminar_bulk_create',
                    ),
                ] + urls
        return  urls


    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Modify foreign key querysets to also be resticted.
        """
        field = super(SeminarAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['speaker', 'title', ]:
            field.help_text += ' (leave blank if this is not known &mdash; do <strong>not</strong> use TBA)'
        return field


    def view_on_site(self, obj):
        return obj.get_absolute_url()


    def get_object(self, *args, **kwargs):
        """
        Mangle the slug when the speaker and title are not both set.
        """
        obj = super(SeminarAdmin, self).get_object(*args, **kwargs)
        if not (obj.speaker and obj.title):
            obj.slug = ''
        self._object = obj # capture for later use.
        return obj



admin.site.register(Seminar, SeminarAdmin)


##########################################################################

class SeminarCancelAdmin(admin.ModelAdmin):
    list_display = ['when', 'message',]
    list_filter = ['when', ]
    ordering = ['-when', ]

# admin.site.register(SeminarCancelAnnouncement, SeminarCancelAdmin)


##########################################################################
