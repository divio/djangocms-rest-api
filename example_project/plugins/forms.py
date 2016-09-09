# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import forms

from plugins.models import ContactRequest


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactRequest
        fields = '__all__'
