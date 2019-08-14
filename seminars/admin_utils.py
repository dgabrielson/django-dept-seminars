"""
Reusable admin helpers (not mixin classes).
"""
##########################################################################
from __future__ import unicode_literals

from django.contrib import admin

##########################################################################

class UsedValuesForeignKeyFilter(admin.SimpleListFilter):
    """
    A custom filter, so that we only see foreign key values which are used.
    """
    # Define a subclass and set these appropriately:
    title = 'SetThis'
    parameter_name = 'set_this__id__exact'
    field_name = 'set_this'
    allow_none = True
    model = object
 
    def get_filter_name(self, obj):
        """
        Return the name of the object, as appropriate
        """
        return "{}".format(obj)

    def get_lookup_values_queryset(self, request, model_admin):
        """
        Return the related objects queryset to use for the filter.
        """
        qs = model_admin.get_queryset(request)
        pk_set = qs.values_list(self.field_name, flat=True).distinct()
        related_qs = self.model.objects.filter(pk__in=pk_set)
        return related_qs
        
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples (coded-value, title).
        """
        related_qs = self.get_lookup_values_queryset(request, model_admin)
        lookups = [ (o.pk, self.get_filter_name(o)) for o in related_qs ]
        if self.allow_none:
            lookups.append(('(None)', '(None)'))
        return lookups

                 
    def queryset(self, request, queryset):
        """
        Apply the filter to the existing queryset.
        """
        filter = self.value()
        filter_field = self.field_name
        if filter is None:
            return
        elif filter == '(None)':
            filter_field += '__isnull'
            filter_value = True
        else:
            filter_field += '__pk__exact'
            filter_value = filter
        return queryset.filter(**{filter_field: filter_value})

##############################################################
