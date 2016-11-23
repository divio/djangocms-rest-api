# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings


plugin_serializer_mapping = {}


if 'cmsplugin_filer_image' in settings.INSTALLED_APPS:
    from cmsplugin_filer_image.cms_plugins import FilerImagePlugin
    from djangocms_rest_api.serializers.filerimageplugin_serializer import FilerImagePluginSerializer

    plugin_serializer_mapping[FilerImagePlugin.__name__] = FilerImagePluginSerializer

