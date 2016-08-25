# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.models import Page, Placeholder, CMSPlugin
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import viewsets

from djangocms_rest_api.serializers import (
    PageSerializer, PlaceHolderSerializer, BasePluginSerializer, get_serializer, get_serializer_class
)
from djangocms_rest_api.views.utils import QuerysetMixin


class PageViewSet(QuerysetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()

    def get_queryset(self):
        site = get_current_site(self.request)
        if self.request.user.is_staff:
            return Page.objects.drafts().on_site(site=site).distinct()
        else:
            return Page.objects.public().on_site(site=site).distinct()


class PlaceHolderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceHolderSerializer
    queryset = Placeholder.objects.all()

    def get_queryset(self):
        site = get_current_site(self.request)
        if self.request.user.is_staff:
            return Placeholder.objects.filter(page__publisher_is_draft=True, page__site=site).distinct()
        else:
            return Placeholder.objects.filter(page__publisher_is_draft=False, page__site=site).distinct()


class PluginViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BasePluginSerializer
    queryset = CMSPlugin.objects.all()

    def get_object(self):
        obj = super(PluginViewSet, self).get_object()
        instance, plugin = obj.get_plugin_instance()
        return instance

    def get_serializer_class(self):
        # TODO: decide if we need custom serializer here
        if self.action == 'retrieve':
            obj = self.get_object()
            # Do not use model here, since it replace base serializer with quire limited created from model
            return get_serializer_class(plugin=obj.get_plugin_class())
        return super(PluginViewSet, self).get_serializer_class()




