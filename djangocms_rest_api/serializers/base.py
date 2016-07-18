# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

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
        return reverse('page-detail', args=(obj.pk,))

    def get_redirect(self, obj):
        return obj.get_redirect(self.language)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = PageSerializer(*args, **kwargs)
        return ListSerializer(*args, **kwargs)


class BasePluginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CMSPlugin
        fields = ['placeholder', 'parent', 'position', 'language', 'plugin_type', 'creation_date', 'changed_date', ]

        
class PlaceHolderSerializer(RequestSerializer, serializers.ModelSerializer):
    plugins = serializers.SerializerMethodField()

    class Meta:
        model = Placeholder
        fields = ['slot', 'default_width', 'plugins']

    def get_plugins(self, obj):
        return [plugin.id for plugin in obj.get_plugins(self.language)]
