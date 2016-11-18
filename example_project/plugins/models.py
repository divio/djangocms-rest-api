# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from six import python_2_unicode_compatible


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
