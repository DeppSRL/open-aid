from django.db import models
from rest_framework import serializers
from rest_framework import fields


class TranslatedModelSerializer(serializers.HyperlinkedModelSerializer):

    def get_field(self, model_field):
        kwargs = {}
        if issubclass(
                model_field.__class__,
                      (models.CharField,
                       models.TextField)):
            if model_field.null:
                kwargs['allow_none'] = True
            kwargs['max_length'] = getattr(model_field, 'max_length')
            return fields.CharField(**kwargs)
        return super(TranslatedModelSerializer, self).get_field(model_field)

    # def __init__(self, *args, **kwargs):
    #     super(TranslateSerializer, self).__init__(*args, **kwargs)
    #     self.translate_fields = getattr(self.Meta, 'translate_fields', ())
    #     if kwargs.get('context', None):
    #         if kwargs['context'].get('request', None) and kwargs['context'].get('request').get('LANGUAGE_CODE', None):
    #             self.lang = self.lang.LANGUAGE_CODE
    #
    # def to_native(self, obj):
    #     # Exclude ALWAYS language specific fields
    #     for language in settings.LANGUAGES:
    #         if language[0] != 'en':
    #             for field in self.translate_fields:
    #                 key = field + '_' + language[0]
    #                 if self.fields.get(key):
    #                     self.fields.pop(key)
    #
    #     ret = super(serializers.ModelSerializer, self).to_native(obj)
    #
    #     # Get current language and give the fields
    #     if self.lang != 'en':
    #         for field in self.translate_fields:
    #             trans = getattr(obj, field + "_" + self.lang)
    #             if trans:
    #                 ret[field] = trans
    #     return ret
    #
    # def from_native(self, data, files):
    #     instance = getattr(self, 'object', None)
    #     if self.lang != 'en':
    #         for field in self.translate_fields:
    #             value = data.get(field) or None
    #             if value:
    #                 data[field + "_" + self.lang] = value
    #                 # If is instance (existent object), set the original attr
    #                 data[field] = getattr(instance, field, data[field])
    #
    #     ret = super(serializers.ModelSerializer, self).from_native(data, files)
    #     return ret
