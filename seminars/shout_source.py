from __future__ import unicode_literals

import shouts

from .context_processors import get_queryset

##
## NOTE:
##  * You cannot use reverse() url matching here, since autodiscover()
##      is typically called in the url conf, and thus patterns may not
##      be loaded yet. [UNLESS shouts.autodiscover() is **last**.]
##


shouts.sources.register('Upcoming Seminar', get_queryset,
                        # verbose_name=..., # default
                        template_name='seminars/shouts/%s.html',
                        url='/seminars/',
                        pubdate_field_name='modified',
                        dtstart_field_name='when')
