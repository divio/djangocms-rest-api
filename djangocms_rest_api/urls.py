# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.routers import DefaultRouter

from djangocms_rest_api.views import PageViewSet, PlaceHolderViewSet, PluginViewSet

router = DefaultRouter()
router.register(r'pages', PageViewSet, 'page')
router.register(r'placeholders', PlaceHolderViewSet, 'placeholder')
router.register(r'plugins', PluginViewSet, 'plugin')
urlpatterns = router.urls
