# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import mimetypes
import os
import re

from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from djangocms_forms.models import FormSubmission
from ipware.ip import get_ip
from rest_framework.exceptions import ValidationError
from unidecode import unidecode
from djangocms_forms.forms import FormBuilder
from rest_framework import serializers
from rest_framework.fields import empty
from djangocms_forms.signals import form_submission
from djangocms_forms.uploads import handle_uploaded_files


def validate_file(uploaded_file, name, required=False, allowed_file_types=None, *args, **kwargs):
    max_upload_size = settings.DJANGOCMS_FORMS_MAX_UPLOAD_SIZE
    allowed_file_types = allowed_file_types or settings.DJANGOCMS_FORMS_ALLOWED_FILE_TYPES

    allowed_file_types = [i.lstrip('.').lower()
                          for i in allowed_file_types]

    if not uploaded_file:
        if required:
            raise ValidationError({name: _('This field is required.')})
        return uploaded_file

    if not os.path.splitext(uploaded_file.name)[1].lstrip('.').lower() in allowed_file_types:
        raise ValidationError(
            {name: _('Sorry, this filetype is not allowed. Allowed filetype: %s') % ', '.join(allowed_file_types)})

    if uploaded_file._size > max_upload_size:
        params = {
            'max_size': filesizeformat(max_upload_size),
            'size': filesizeformat(uploaded_file._size)
        }
        msg = _(
            'Please keep file size under %(max_size)s. Current size is %(size)s.') % params
        raise ValidationError({name: msg})

    return uploaded_file


class FormBuilderMixin(object):

    def __init__(self, *args, **kwargs):
        super(FormBuilderMixin, self).__init__(*args, **kwargs)
        self.field_names = []
        self.file_fields = []
        self.field_types = {}
        self.file_field_params = {}

    def save_to_db(self, form_data, request, referrer):
        user = request.user if request.user.is_authenticated() else None
        FormSubmission.objects.create(
            plugin=self.form_definition.plugin_reference,
            ip=get_ip(request),
            referrer=referrer,
            form_data=form_data,
            created_by=user)

    def email_submission(self, form_data, request, referrer):
        mail_to = re.compile('\s*[,;]+\s*').split(self.form_definition.email_to)
        mail_from = self.form_definition.email_from or None
        mail_subject = self.form_definition.email_subject or \
            'Form Submission - %s' % self.form_definition.name
        context = {
            'form': self.form_definition,
            'referrer': referrer,
            'title': mail_subject,
            'form_data': form_data,
            'request': request,
            'recipients': mail_to,
        }

        message = render_to_string('djangocms_forms/email_template/email.txt', context)
        message_html = render_to_string('djangocms_forms/email_template/email.html', context)

        email = EmailMultiAlternatives(mail_subject, message, mail_from, mail_to)
        email.attach_alternative(message_html, 'text/html')

        if self.form_definition.email_uploaded_files:
            if hasattr(self, 'files'):
                files = self.files.values()
            else:
                files = [self.cleaned_data[field] for field in self.file_fields]

            for file_obj in files:
                file_obj.open('r')
                content = file_obj.read()
                file_obj.close()
                content_type = getattr(file_obj, 'content_type', None)
                if not content_type:
                    path = getattr(file_obj, 'path', None)
                    if not path:
                        path = getattr(file_obj.file, 'path', '')
                    content_type, _ = mimetypes.guess_type(os.path.basename(path))
                email.attach(file_obj.name, content, content_type)

        email.send(fail_silently=False)

    def get_unique_field_name(self, field):
        field_name = field.field_name or field.label
        field_name = '%s' % (slugify(unidecode(field_name).replace('-', '_')))

        if field_name in self.field_names:
            i = 1
            while True:
                if i > 1:
                    if i > 2:
                        field_name = field_name.rsplit('_', 1)[0]
                    field_name = '%s_%s' % (field_name, i)
                if field_name not in self.field_names:
                    break
                i += 1

        self.field_names.append(field_name)
        self.field_types[field_name] = field.field_type
        return field_name


class FormPluginDataSerializer(FormBuilderMixin, serializers.Serializer):
    """
    I'm seriously doubt about writing serializers for external plugins like this and adding them to rest api code

    serializer for forms plugin https://github.com/mishbahr/djangocms-forms

    """

    def __init__(self, *args, **kwargs):
        super(FormPluginDataSerializer, self).__init__(*args, **kwargs)
        self.form_definition = self.plugin_instance = self.context.get('plugin_instance', None)
        self.plugin = self.context.get('plugin', None)
        depth = 0
        for field in self.form_definition.fields.all():

            field_name = self.get_unique_field_name(field)

            self.fields[field_name] = self.get_field(field, field_name)

    field_mapping = {
        'text': serializers.CharField,
        'textarea': serializers.CharField,
        'email': serializers.EmailField,
        'number': serializers.IntegerField,
        'phone': serializers.CharField,
        'url': serializers.URLField,
        'checkbox': serializers.BooleanField,
        'checkbox_multiple': serializers.MultipleChoiceField,
        'select': serializers.ChoiceField,
        'radio': serializers.ChoiceField,
        'file': serializers.FileField,
        'date': serializers.DateField,
        'time': serializers.TimeField,
        'password': serializers.CharField,
        'hidden': serializers.CharField,
    }

    def get_field(self, field, field_name):
        """
        Create regular model fields.
        """

        field_class = self.field_mapping[field.field_type]
        field_kwargs = field.build_field_attrs()
        field_kwargs['allow_null'] = not field_kwargs.get('required', True)
        field_kwargs['initial'] = field_kwargs.get('initial', None) or empty

        if field.field_type == 'file':
            self.file_fields.append(field_name)
            if field.choice_values:
                regex = re.compile('[\s]*\n[\s]*')
                choices = regex.split(field.choice_values)
                allowed_file_types = [i.lstrip('.').lower() for i in choices]
                self.file_field_params[field_name] = {'allowed_file_types': allowed_file_types}

        elif issubclass(field_class, (serializers.ChoiceField, serializers.MultipleChoiceField)):
            choices = field.get_choices() or []
            if field.field_type == 'select' and not field_kwargs['required']:
                choices.insert(0, ('', ''))
            field_kwargs['choices'] = choices

        if issubclass(field_class, serializers.CharField) or issubclass(field_class, serializers.ChoiceField):
            # `allow_blank` is only valid for textual fields.
            field_kwargs['allow_blank'] = not field_kwargs.get('required', True)
        if issubclass(field_class, serializers.BooleanField):
            field_kwargs['initial'] = FormBuilder.to_bool(None, field_kwargs['initial'])
        return field_class(**field_kwargs)

    def validate(self, attrs):
        attrs = super(FormPluginDataSerializer, self).validate(attrs)
        for field in self.file_fields:
            validate_file(
                attrs[field], name=field, required=self.fields[field].required, **self.file_field_params.get(field, {}))
        return attrs

    def save(self, **kwargs):
        return super(FormPluginDataSerializer, self).save(**kwargs)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        # TODO: replace this hack or check if it is fine
        self.cleaned_data = validated_data

        handle_uploaded_files(self)
        form_data = []
        for field in self.field_names:
            if field not in validated_data:
                continue
            value = validated_data[field]
            if hasattr(value, 'url'):
                value = value.url
            form_data.append({
                'name': field,
                'label': self.fields[field].label,
                'value': value,
                'type': self.field_types[field],
            })

        referrer = validated_data.get('referrer', '')

        request = self.context['request']

        if self.form_definition.save_data:
            self.save_to_db(form_data, request=request, referrer=referrer)
        if self.form_definition.email_to:
            self.email_submission(form_data, request=request, referrer=referrer)
        form_submission.send(
            sender=self.context['view'].__class__, form=self.form_definition, cleaned_data=validated_data)

        return validated_data


