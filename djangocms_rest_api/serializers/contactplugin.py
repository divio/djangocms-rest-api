# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from django.utils.translation import ugettext as _

from rest_framework import serializers


class ContactPluginDataSerializer(serializers.Serializer):
    """
    I'm seriously doubt about writing serializers for external plugins like this and adding them to rest api code
    """
    email = serializers.EmailField(label=_("Email"))
    subject = serializers.CharField(label=_("Subject"), required=False, allow_null=True)
    content = serializers.CharField(label=_("Content"), )

    def save(self, **kwargs):
        plugin_instance = self.context.get('plugin_instance', None)
        plugin = self.context.get('plugin', None)

        plugin.send(self, plugin_instance.form_name, plugin_instance.site_email)

    @property
    def cleaned_data(self):
        return self.data
