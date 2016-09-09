# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import random

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.conf import settings
from django.contrib import admin
from sekizai.context import SekizaiContext

from mixins import RESTPluginMixin
from plugins.forms import ContactForm
from plugins.models import Slide, Slider, ContactRequest, Contact
from plugins.serializers import SliderWithInlinesPluginSerializer, ContactRequestSerializer


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


class ContactFormPlugin(RESTPluginMixin, CMSPluginBase):
    model = Contact
    name = 'ContactForm'
    form = ContactForm
    render_template = 'plugins/contact_form.html'
    data_serializer_class = ContactRequestSerializer

    def render(self, context, instance, placeholder):
        request = context['request']
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                self.process_post(request, instance, form)
                form = ContactForm()

        else:
            form = ContactForm()
        context.update({
            'form': form,
            'instance': instance
        })
        return context

    def process_data(self, request, instance, serializer):
        # Check instance form class, serializer class? do action?
        serializer.save()

plugin_pool.register_plugin(ContactFormPlugin)
