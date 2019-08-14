#########################################################################
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

#########################################################################

class SeminarsConfig(AppConfig):
    name = "seminars"
    verbose_name = _("Seminars")

    def ready(self):
        """
        Any app specific startup code, e.g., register signals,
        should go here.
        """

#########################################################################
