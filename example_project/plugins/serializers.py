# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers

from plugins.models import Slider, ContactRequest


class SliderWithInlinesPluginSerializer(serializers.ModelSerializer):
    """
    Serializer class for slider plugin
    """

    test = serializers.SerializerMethodField()

    class Meta:
        model = Slider
        depth = 1
        fields = ['id', 'name', 'slides', 'test']

    def get_test(self, obj):
        return 'test'


class ContactRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactRequest
        fields = ['sender', 'subject', 'message']
