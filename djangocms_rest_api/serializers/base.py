# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from collections import OrderedDict

from classytags.utils import flatten_context
from cms.models import Page, Placeholder, CMSPlugin
from django.core.urlresolvers import reverse
from rest_framework import serializers
from rest_framework.serializers import ListSerializer
from djangocms_rest_api.serializers.utils import RequestSerializer


class PageSerializer(RequestSerializer, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    page_title = serializers.SerializerMethodField()
    menu_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()
    languages = serializers.ListField(source='get_languages')
    url = serializers.SerializerMethodField()
    redirect = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'placeholders', 'creation_date', 'changed_date', 'publication_date',
            'publication_end_date', 'in_navigation', 'template', 'is_home', 'languages', 'parent',
            'site', 'page_title', 'menu_title', 'meta_description', 'slug', 'url', 'path',
            'absolute_url', 'redirect'
        ]

    def get_title(self, obj):
        return obj.get_title(self.language)

    def get_page_title(self, obj):
        return obj.get_page_title(self.language)

    def get_menu_title(self, obj):
        return obj.get_menu_title(self.language)

    def get_meta_description(self, obj):
        return obj.get_meta_description(self.language)

    def get_slug(self, obj):
        return obj.get_slug(self.language)

    def get_path(self, obj):
        return obj.get_path(self.language)

    def get_template(self, obj):
        return obj.get_template()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url(self.language)

    def get_url(self, obj):
        return reverse('api:page-detail', args=(obj.pk,))

    def get_redirect(self, obj):
        return obj.get_redirect(self.language)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = PageSerializer(*args, **kwargs)
        return ListSerializer(*args, **kwargs)


# TODO: replace with better implementation
def modelserializer_factory(mdl, fields=None, **kwargs):

    def _get_declared_fields(attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, serializers.Field)]
        fields.sort(key=lambda x: x[1]._creation_counter)
        return OrderedDict(fields)

    class Base(object):
        pass

    Base._declared_fields = _get_declared_fields(kwargs)

    class SerializerClass(Base, serializers.ModelSerializer):
        class Meta:
            model = mdl

        if fields:
            setattr(Meta, "fields", fields)

    return SerializerClass


# TODO: Add support for items with children (child_plugin_instances)
# TODO: Check image plugin data serializer
# TODO: decide if we need to return url for images with domain name or nor
class BasePluginSerializer(serializers.ModelSerializer):

    plugin_data = serializers.SerializerMethodField()
    inlines = serializers.SerializerMethodField()

    class Meta:
        model = CMSPlugin
        fields = ['id', 'placeholder', 'parent', 'position', 'language', 'plugin_type', 'creation_date', 'changed_date',
                  'plugin_data', 'inlines', ]

    def get_plugin_data(self, obj):

        instance, plugin = obj.get_plugin_instance()
        model = getattr(plugin, 'model', None)
        if model:
            serializer = modelserializer_factory(getattr(plugin, 'model', None))(instance)
            return serializer.data
        return {}

    def get_inlines(self, obj):
        instance, plugin = obj.get_plugin_instance()
        inlines = getattr(plugin, 'inlines', [])
        data = {}
        for inline in inlines:
            for related_object in instance._meta.related_objects:
                if getattr(related_object, 'related_model', None) == inline.model:
                    name = related_object.name
                    serializer = modelserializer_factory(inline.model)(getattr(instance, name).all(), many=True)
                    data[name] = serializer.data
                    break
        return data


class SimplePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', ]


class PlaceHolderSerializer(RequestSerializer, serializers.ModelSerializer):
    plugins = serializers.SerializerMethodField()
    page = SimplePageSerializer()

    class Meta:
        model = Placeholder
        fields = ['id', 'slot', 'plugins', 'page']
        depth = 2

    def get_plugins(self, obj):
        return [plugin.id for plugin in obj.get_plugins(self.language)]
