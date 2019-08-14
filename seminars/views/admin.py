"""
Admin views for the seminars application.
"""
#######################################################################
from __future__ import unicode_literals

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView

from .. import conf
from ..forms import BulkCreateSeminarForm
from ..mixins import RestrictedFormViewMixin, SingleFKFormViewMixin

#######################################################################
#######################################################################
#######################################################################

class BulkCreateSeminarAdminView(SingleFKFormViewMixin, RestrictedFormViewMixin,
                                 FormView):
    """
    For bulk creating seminars.
    """
    form_class = BulkCreateSeminarForm
    login_required = True
    template_name = 'admin/seminars/seminar/bulk_create_form.html'
    success_url = reverse_lazy('admin:seminars_seminar_changelist')
    admin_context = {}
    # restricted form
    is_restricted_user = conf.get('user_is_admin_restricted')
    restricted_user_filter = conf.get('seminar:user_filter')
    restricted_exclude_fields = conf.get('seminar:restricted_fields')
    restricted_foreign_key_fields = {'series': conf.get('series:user_filter')}
    restricted_extra_filters = conf.get('seminar:restricted_extra_filters')
    # single fk
    single_fk_src = 'series'
    single_fk_initial = {}


    def form_valid(self, form):
        """
        Define form valid, rather than a success url, because a valid
        form returns the spreadsheet.
        """
        results = form.on_success()
        messages.success(self.request, 
                         _('Added %(count)d %(desc)s') % {
                                'count': len(results), 
                                'desc': _('seminars')}, 
                         fail_silently=True)
        return super(BulkCreateSeminarAdminView, self).form_valid(form)


#######################################################################

class HelpAdminView(TemplateView):
    pass
    
class SeminarSeriesOrganizerHelpAdminView(HelpAdminView):
    template_name = 'admin/seminars/seminarseries/organizer_help.html'

#######################################################################
#######################################################################
#######################################################################
