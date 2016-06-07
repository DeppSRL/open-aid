from django.conf import settings
from django.utils import translation
from haystack import connections
from haystack.backends.solr_backend import SolrEngine, SolrSearchBackend, SolrSearchQuery
from haystack.constants import DEFAULT_ALIAS

def get_using(language, alias=DEFAULT_ALIAS):
    new_using = alias + "_" + language
    using = new_using if new_using in settings.HAYSTACK_CONNECTIONS else alias
    return using


class MultilingualSolrSearchBackend(SolrSearchBackend):
    def update(self, index, iterable, commit=True):
        # keep starting language
        initial_language = translation.get_language()[:2]

        if self.connection_alias in ('default', 'initiative'):
            # default connection is for settings.LANGUAGE_CODE[:2] (LANG_CODE)
            language = settings.LANG_CODE
        else:
            # connection for other languages
            language = self.connection_alias[-2:]

        # active the language to use django-modeltranslation magic fields (*_en, *_it)
        translation.activate(language)
        # call the default solr update method
        super(MultilingualSolrSearchBackend, self).update(index, iterable, commit=commit)
        # rollback to the starting language
        translation.activate(initial_language)


class MultilingualSolrSearchQuery(SolrSearchQuery):
    def __init__(self, using=DEFAULT_ALIAS):
        language = translation.get_language()[:2]
        using = get_using(language)
        super(MultilingualSolrSearchQuery, self).__init__(using)


class MultilingualSolrEngine(SolrEngine):
    backend = MultilingualSolrSearchBackend
    query = MultilingualSolrSearchQuery
