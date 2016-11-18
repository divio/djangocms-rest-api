# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from plugins.models import Slide, Slider
from plugins.serializers import SliderWithInlinesPluginSerializer


class SlideInlineAdmin(admin.StackedInline):
    model = Slide


class SliderWithInlinesPlugin(CMSPluginBase):
    """
    Sample Slider plugin, to test inlines processing with API
    no styles and scrips, since it is not important for api
    """
    model = Slider
    name = 'Slider'
    render_template = 'plugins/slider.html'
    inlines = (SlideInlineAdmin,)

    def render(self, context, instance, placeholder):
        slides = instance.slides.all()
        context.update({
            'slides': slides,
            'instance': instance,
            'MEDIA_URL': settings.MEDIA_URL
        })
        return context

plugin_pool.register_plugin(SliderWithInlinesPlugin)


class SliderPlugin(CMSPluginBase):
    """
    Plugin with predefined serializer class for API
    """
    model = Slider
    name = 'Slider'
    render_template = 'plugins/slider.html'
    inlines = (SlideInlineAdmin,)
    serializer_class = SliderWithInlinesPluginSerializer

    def render(self, context, instance, placeholder):
        slides = instance.slides.all()
        context.update({
            'slides': slides,
            'instance': instance,
            'MEDIA_URL': settings.MEDIA_URL
        })
        return context

plugin_pool.register_plugin(SliderPlugin)
