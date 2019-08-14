"""
Forms for the seminars application.
"""
#######################################################################
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe

from markuphelpers.forms import LinedTextareaWidget, ReStructuredTextFormMixin

from . import conf
from .models import Seminar, SeminarSeries

#######################################################################

class AdminSeminarSeriesForm(ReStructuredTextFormMixin, forms.ModelForm):
    """
    The form for seminars in the Django admin.
    """
    restructuredtext_fields = [ ('description', True), ]
    
    class Meta:
        model = Seminar
        widgets = {
                'description': LinedTextareaWidget(attrs={'rows': 11, 'cols': 100}),
            } 
        exclude = []
    

#######################################################################

class AdminSeminarForm(ReStructuredTextFormMixin, forms.ModelForm):
    """
    The form for seminars in the Django admin.
    """
    restructuredtext_fields = [ ('abstract', True), ]
    
    class Meta:
        model = Seminar
        widgets = {
                'abstract': LinedTextareaWidget,
                'when': AdminSplitDateTime,
                'speaker': forms.TextInput(attrs={'size': 35}),
                'affiliation': forms.TextInput(attrs={'size': 70}),
                'title': forms.TextInput(attrs={'size': 70}),
                'abstract_url': forms.TextInput(attrs={'size': 70}),
                'note': forms.TextInput(attrs={'size': 70}),
            } 
        field_classes = {
            'when': forms.SplitDateTimeField,
            }
        exclude = []
    

#######################################################################


class SeminarForm(AdminSeminarForm): 
    """
    A form for adding and updating seminars.
    Uses the Admin widgets for datetime.

    Note, due to the way Form Media is implemented,
    include the following lines *first*:

    {{ form.pre_media }}
    {{ form.media }}
    """
    class Media:
        css = {'all': (
                    staticfiles_storage.url("admin/css/widgets.css"),
                    staticfiles_storage.url("css/forms.css"),
                    staticfiles_storage.url("css/twoColumn.css"),
                ),
            }

        
#######################################################################

class BulkCreateSeminarForm(forms.Form):
    """
    Funding Report input form.
    """
    series = forms.ModelChoiceField(required=True, queryset=SeminarSeries.objects.active())
    start_date = forms.DateField(required=True, widget=AdminDateWidget())
    end_date = forms.DateField(required=True, widget=AdminDateWidget())
            

    def on_success(self):
        """
        Called when form is valid.   Actually do bulk create here.
        """
        d = self.cleaned_data['start_date']
        seminarseries = self.cleaned_data['series']
        # if necessary, advance dt until day of week is default:
        while d.isoweekday() != seminarseries.default_dayofweek:
            d += timedelta(days=1)
        
        initial = []
        # create initial_data:
        while d <= self.cleaned_data['end_date']:
            dt = datetime.combine(d, seminarseries.default_time)
            when = timezone.make_aware(dt)
            initial.append(Seminar(when=when, 
                                   location=seminarseries.default_location, 
                                   series=seminarseries))
            if seminarseries.default_interval < 1:
                break
            d += timedelta(days=seminarseries.default_interval)
            
        return Seminar.objects.bulk_create(initial)


#######################################################################
