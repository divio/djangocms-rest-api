# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from itertools import chain

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from cms.models import Page, Placeholder, CMSPlugin
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from djangocms_rest_api.serializers import (
    PageSerializer, PlaceHolderSerializer, BasePluginSerializer, get_serializer, get_serializer_class, get_data_serializer_class
)
from djangocms_rest_api.views.utils import QuerysetMixin, check_if_page_is_visible
from djangocms_rest_api.serializers.mapping import data_serializer_class_mapping


class PageViewSet(QuerysetMixin, viewsets.ReadOnlyModelViewSet):
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
        is_visible = check_if_page_is_visible(self.request, page)
        if not is_visible:
            raise PermissionDenied(_('You are not allowed to se this page'))

        self.obj = obj
        # TODO: check if plugin available for anonymous or current user
        self.instance, self.plugin = obj.get_plugin_instance()
        # Not sure we ned this permissions for retrieve data actions
        if self.action == 'submit_data':
            obj_permissions = [permission() for permission in getattr(self.instance, 'permission_classes', [])]
            for permission in obj_permissions:
                if not permission.has_object_permission(self.request, self, obj):
                    self.permission_denied(
                        self.request, message=getattr(permission, 'message', None)
                    )
        return self.instance

    def get_serializer_class(self):
        # TODO: decide if we need custom serializer here
        if self.action == 'retrieve':
            obj = self.get_object()
            # Do not use model here, since it replaces base serializer with quite limited one, created from model
            return get_serializer_class(plugin=obj.get_plugin_class())
        return super(PluginViewSet, self).get_serializer_class()

    def get_data_serializer_context(self):
        context = self.get_serializer_context()
        assert self.instance, 'get object should be called before this method'
        assert self.plugin, 'get object should be called before this method'
        context['plugin'] = self.plugin
        context['plugin_instance'] = self.instance
        return context

    @detail_route(methods=['post', 'put', 'patch'])
    def submit_data(self, request, pk=None, **kwargs):
        # TODO: need ability to handle nested pks
        obj = self.get_object()
        serializer_class = get_data_serializer_class(self.plugin)

        assert serializer_class, 'data serializer class should be set'
        if request.method == 'POST':
            serializer = serializer_class(
                data=request.data, context=self.get_data_serializer_context())
        else:
            raise PermissionDenied('method is not allowed for now')
        if serializer.is_valid():
            if hasattr(self.instance, 'process_data'):
                self.instance.process_data(request, self.instance, serializer)
            else:
                # TODO: Decide if we need to save data by default if process_data method was not implemented
                # point this in documentation.
                # Save can just do any action
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


