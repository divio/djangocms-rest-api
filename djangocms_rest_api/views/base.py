# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext as _
from cms.models import Page, Placeholder, CMSPlugin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from djangocms_rest_api.serializers import (
    PageSerializer, PlaceHolderSerializer, BasePluginSerializer, get_serializer_class
)
from djangocms_rest_api.views.utils import check_if_page_is_visible


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()

    def get_queryset(self):
        site = get_current_site(self.request)
        if self.request.user.is_staff:
            return Page.objects.drafts().on_site(site=site).distinct()
        else:
            return Page.objects.public().on_site(site=site).distinct()


class PlaceHolderViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        Do not use list for now, add later if required
    """
    queryset = Placeholder.objects.all()
    serializer_class = PlaceHolderSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_object(self):
        obj = super(PlaceHolderViewSet, self).get_object()
        page = obj.page
        if not page:
            raise PermissionDenied()
        is_visible = check_if_page_is_visible(self.request, page)
        if not is_visible:
            raise PermissionDenied(_('You are not allowed to se this page'))
        return obj


class PluginViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        Do not use list for now, add later if required
    """
    serializer_class = BasePluginSerializer
    queryset = CMSPlugin.objects.all()

    def get_object(self):
        obj = super(PluginViewSet, self).get_object()
        page = obj.placeholder.page
        if not page:
            raise PermissionDenied()
        is_visible = check_if_page_is_visible(self.request, page)
        if not is_visible:
            raise PermissionDenied(_('You are not allowed to se this page'))

        instance, plugin = obj.get_plugin_instance()
        return instance

    def get_serializer_class(self):
        # TODO: decide if we need custom serializer here
        if self.action == 'retrieve':
            obj = self.get_object()
            # Do not use model here, since it replaces base serializer with quite limited one, created from model
            return get_serializer_class(plugin=obj.get_plugin_class())
        return super(PluginViewSet, self).get_serializer_class()



