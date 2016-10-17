# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.models import CMSPlugin
from django.db import models
from six import python_2_unicode_compatible
from cmsplugin_contact.models import BaseContact
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Slider(CMSPlugin):
    """
    Slider for showing slides.
    Name will be show on the page.
    """
    name = models.CharField(_('name'), max_length=60)

    def __str__(self):
        return self.name

    def copy_relations(self, old_instance):
        for slide in old_instance.slides.all():
            slide.pk = None
            slide.slider = self
            slide.save()


@python_2_unicode_compatible
class Slide(models.Model):
    """
    Slide for slider. Each slide will be connected with parent slider.
    """
    title = models.CharField(max_length=60, help_text='Title')
    image = models.ImageField(upload_to='images/slides/', blank=True)
    slider = models.ForeignKey(Slider, related_name='slides')
    sequence_number = models.IntegerField(default=0,
                                          help_text='Sequence number of slide '
                                                    'in slide show')

    class Meta:
        ordering = ['sequence_number', 'pk']

    def __str__(self):
        return '%s %s' % (self.title, self.slider.name)


@python_2_unicode_compatible
class Contact(CMSPlugin):
    form_name = models.CharField(verbose_name=_('form name'), max_length=255)

    def __str__(self):
        return self.form_name


@python_2_unicode_compatible
class ContactRequest(models.Model):
    """
    Model which stores contact request and messages
    """
    sender = models.EmailField(verbose_name=_('email'))
    subject = models.CharField(verbose_name=_('subject'), max_length=255)
    message = models.TextField(verbose_name=_('message'))

    def __str__(self):
        return '{} {}'.format(self.sender, self.subject)


class CustomContact(BaseContact):
    custom_label = models.CharField(
        _('Custom sender label'),
        default=_('Your custom value'), max_length=20)
