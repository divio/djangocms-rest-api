# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cmsplugin_filer_image.models import FilerImage
from rest_framework import serializers


class FilerImagePluginSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilerImage
        depth = 1
        fields = '__all__'
