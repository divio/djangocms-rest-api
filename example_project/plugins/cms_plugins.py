# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_contact.cms_plugins import ContactPlugin
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from djangocms_rest_api.mixins import RESTPluginMixin
from plugins.forms import ContactForm
from plugins.models import CustomContact
from plugins.models import Slide, Slider, Contact
from plugins.serializers import SliderWithInlinesPluginSerializer, ContactRequestSerializer
from djangocms_rest_api.serializers.contactplugin import ContactPluginDataSerializer


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
                self.process_data(request, instance, form)
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


class CustomContactPlugin(ContactPlugin):
    name = _("Custom Contact Form")

    model = CustomContact

    data_serializer_class = ContactPluginDataSerializer

    fieldsets = (
        (None, {
            'fields': ('form_name', 'form_layout', 'site_email', 'submit', 'custom_label'),
        }),
        (_('Redirection'), {
            'fields': ('thanks', 'redirect_url'),
        }),
        (_('Spam Protection'), {
            'fields': ('spam_protection_method', 'akismet_api_key',
                       'recaptcha_public_key', 'recaptcha_private_key', 'recaptcha_theme')
        })
    )


plugin_pool.register_plugin(CustomContactPlugin)
