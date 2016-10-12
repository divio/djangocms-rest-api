# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
from cms.api import create_page, add_plugin
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from djangocms_forms.models import FormField
from filer.models import Image
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import status

from plugins.models import Slide, ContactRequest
from tests.utils import CMSApiTestCase
from hamcrest import *


class FormPluginTestCase(CMSApiTestCase):
    """
    Test for plugin from https://github.com/maccesch/cmsplugin-contact
    :return:
    """

    def test_no_data_sent_one_required(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text1', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='text', field_name='text2', required=False)
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {

        }
        response = self.client.post(url, data=data, format='json')
        self.assertIn('text1', response.data)
        self.assertEqual(response.data['text1'], ['This field is required.'])

    def test_data_sent_ok(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='text', field_name='text', required=False)
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'text_2': 'text',
            'text': 'text',
        }
        response = self.client.post(url, data=data, format='json')
        self.assertIn('text', response.data)
        self.assertIn('text_2', response.data)
        self.assertEqual(response.data['text'], 'text')
        self.assertEqual(response.data['text_2'], 'text')

    def test_email_sent(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin', email_to='admin@example.com')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='text', field_name='text', required=False)
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'text_2': 'text2',
            'text': 'text',
        }
        response = self.client.post(url, data=data, format='json')
        self.assertIn('text', response.data)
        self.assertIn('text_2', response.data)
        self.assertEqual(response.data['text'], 'text')
        self.assertEqual(response.data['text_2'], 'text2')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(data['text_2'], mail.outbox[0].body)

    def test_files(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='file', field_name='file', required=True)
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        with open(str(os.path.join(os.path.dirname(__file__), './test-image.jpg')), 'rb') as image:
            data = {
                'text': 'text',
                'file': SimpleUploadedFile('test-image.jpg', image.read(), 'image/jpg')
            }
            response = self.client.post(url, data=data, format='multipart')
        self.assertIn('text', response.data)
        self.assertIn('file', response.data)
        self.assertEqual(response.data['text'], 'text')
        self.assertIn('test-image', response.data['file'])

    def test_email_with_files(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin', email_to='admin@example.com')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='file', field_name='file', required=True)
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        with open(str(os.path.join(os.path.dirname(__file__), './test-image.jpg')), 'rb') as image:
            data = {
                'text': 'text',
                'file': SimpleUploadedFile('test-image.jpg', image.read(), 'image/jpg')
            }
            response = self.client.post(url, data=data, format='multipart')
        self.assertIn('text', response.data)
        self.assertIn('file', response.data)
        self.assertEqual(response.data['text'], 'text')
        self.assertIn('test-image', response.data['file'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(data['text'], mail.outbox[0].body)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertIn('test-image', mail.outbox[0].attachments[0][0])

    def test_files_not_supported_type(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='file', field_name='file', required=True, choice_values='.txt')
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        with open(str(os.path.join(os.path.dirname(__file__), './test-image.jpg')), 'rb') as image:
            data = {
                'text': 'text',
                'file': SimpleUploadedFile('fav.png', image.read(), 'image/png')
            }
            response = self.client.post(url, data=data, format='multipart')
        self.assertIn('file', response.data)
        self.assertEqual(response.data['file'][0], 'Sorry, this filetype is not allowed. Allowed filetype: txt')

    def test_select(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='select', field_name='gender', required=True, choice_values='m\nf')
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        with open(str(os.path.join(os.path.dirname(__file__), './test-image.jpg')), 'rb') as image:
            data = {
                'text': 'text',
                'gender': 'm'
            }
            response = self.client.post(url, data=data, format='multipart')
        print(response.data)
        self.assertIn('text', response.data)
        self.assertIn('gender', response.data)
        self.assertEqual(response.data['text'], 'text')
        self.assertEqual(response.data['gender'], 'm')

    def test_select_invalid_choice(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(form=instance, field_type='select', field_name='gender', required=True, choice_values='m\nf')
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'text': 'text',
            'gender': 'a'
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gender', response.data)
        self.assertEqual(response.data['gender'][0], '"a" is not a valid choice.')

    def test_select_not_required(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(
            form=instance, field_type='select', field_name='gender', required=False, choice_values='m\nf')
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'text': 'text',
            'gender': ''
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text', response.data)
        self.assertIn('gender', response.data)
        self.assertEqual(response.data['text'], 'text')

    def test_checkbox_multiple(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'FormPlugin', 'en', name='sample plugin')
        instance, plugin_model = plugin.get_plugin_instance()

        field1 = FormField(form=instance, field_type='text', field_name='text', required=True)
        field1.save()
        field2 = FormField(
            form=instance, field_type='checkbox_multiple', field_name='type', required=True, choice_values='a\nb\nc')
        field2.save()
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'text': 'text',
            'type': ['a', 'c']
        }
        response = self.client.post(url, data=data, format='json')
        from djangocms_forms.models import FormSubmission
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text', response.data)
        self.assertIn('type', response.data)
        self.assertEqual(response.data['text'], 'text')
        self.assertEqual(response.data['type'], {'a', 'c'})
        submission = FormSubmission.objects.last()
        self.assertIsNotNone(submission.form_data)
        assert_that(submission.form_data, has_item(
             {u'type': u'checkbox_multiple', u'name': u'type', u'value': [u'a', u'c'], u'label': u''}))

