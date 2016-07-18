# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.models import Page, Placeholder, CMSPlugin
from rest_framework import viewsets

from djangocms_rest_api.serializers import (
    PageSerializer, PlaceHolderSerializer, BasePluginSerializer
)
from djangocms_rest_api.views.utils import QuerysetMixin


class PageViewSet(QuerysetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class PlaceHolderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceHolderSerializer
    queryset = Placeholder.objects.all()


class PluginViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BasePluginSerializer
    queryset = CMSPlugin.objects.all()
