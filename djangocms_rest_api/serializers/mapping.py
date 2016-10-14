# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings


serializer_class_mapping = {}
data_serializer_class_mapping = {}


if 'cmsplugin_filer_image' in settings.INSTALLED_APPS:
    from cmsplugin_filer_image.cms_plugins import FilerImagePlugin
    from djangocms_rest_api.serializers.filerimageplugin_serializer import FilerImagePluginSerializer
    serializer_class_mapping[FilerImagePlugin] = FilerImagePluginSerializer


if 'djangocms_forms' in settings.INSTALLED_APPS:
    from djangocms_forms.cms_plugins import FormPlugin
    from djangocms_rest_api.serializers.formplugin import FormPluginDataSerializer
    data_serializer_class_mapping[FormPlugin] = FormPluginDataSerializer

if 'cmsplugin_contact' in settings.INSTALLED_APPS:
    from cmsplugin_contact.cms_plugins import ContactPlugin
    from djangocms_rest_api.serializers.contactplugin import ContactPluginDataSerializer
    data_serializer_class_mapping[ContactPlugin] = ContactPluginDataSerializer
