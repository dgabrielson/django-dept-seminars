#####################################################################

from django import template

from ..models import SeminarSeries

#####################################################################

register=template.Library()

#####################################################################

@register.simple_tag(takes_context=True)
def get_seminar_series(context, save_as=None):
    """
    Only the "show" series.
    {% get_seminar_series %} -> qs
    {% get_seminar_series 'object_list' %}
    """
    qs = SeminarSeries.objects.active().show()
    if save_as is not None:
        context[save_as] = qs
        return ''
    return qs

#####################################################################

@register.simple_tag(takes_context=True)
def get_seminar_series_all(context, save_as=None):
    """
    All the active series.
    {% get_seminar_series_all %} -> qs
    {% get_seminar_series_all 'object_list' %}
    """
    qs = SeminarSeries.objects.active()
    if save_as is not None:
        context[save_as] = qs
        return ''
    return qs

#####################################################################
