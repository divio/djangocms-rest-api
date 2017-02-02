# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if 'rest_framework' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'You must include django rest framework into your installed apps in order to use Django Cms REST API')

GENERIC_PLUGIN_EXCLUDE_FIELDS = getattr(settings, 'CMS_REST_API_GENERIC_PLUGIN_EXCLUDE_FIELDS', [
    'id', 'parent', 'placeholder', 'creation_date', 'changed_date', 'language', ])

GENERIC_PLUGIN_DATA_EXCLUDE_FIELDS = getattr(settings, 'CMS_REST_API_GENERIC_PLUGIN_DATA_EXCLUDE_FIELDS', [
    'plugin_type', 'position', ])
