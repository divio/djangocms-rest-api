# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.models import Page, Placeholder, CMSPlugin
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import viewsets

from djangocms_rest_api.serializers import (
    PageSerializer, PlaceHolderSerializer, BasePluginSerializer
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



