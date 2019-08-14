"""
Haystack search indexes for Seminars application.
"""
###############################################################
from __future__ import unicode_literals

from haystack import indexes

from .models import Seminar

###############################################################

class SeminarIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='modified')
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='speaker')


    def get_model(self, using=None):
        return Seminar


    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.active().exclude_tba()



###############################################################
