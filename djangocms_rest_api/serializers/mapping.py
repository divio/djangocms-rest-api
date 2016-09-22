# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cmsplugin_filer_image.cms_plugins import FilerImagePlugin
from cmsplugin_contact.cms_plugins import ContactPlugin
from djangocms_rest_api.serializers.contactplugin import ContactPluginDataSerializer

from djangocms_rest_api.serializers.filerimageplugin_serializer import FilerImagePluginSerializer

serializer_class_mapping = {
    FilerImagePlugin: FilerImagePluginSerializer,
}

data_serializer_class_mapping = {
    ContactPlugin: ContactPluginDataSerializer
}
