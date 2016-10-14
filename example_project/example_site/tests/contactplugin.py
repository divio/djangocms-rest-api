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


class ContactPluginTestCase(CMSApiTestCase):

    def test_contact_plugin_empty_data_submission(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'ContactFormPlugin', 'en', form_name='contact us')
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'][0], 'This field is required.')
        self.assertIn('subject', response.data)
        self.assertEqual(response.data['subject'][0], 'This field is required.')
        self.assertIn('sender', response.data)
        self.assertEqual(response.data['sender'][0], 'This field is required.')

    def test_contact_plugin_data_submission(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'ContactFormPlugin', 'en', form_name='contact us')
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'message': 'message text',
            'subject': 'subject',
            'sender': 'sender@example.com'
        }
        self.assertEqual(ContactRequest.objects.count(), 0)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContactRequest.objects.count(), 1)
        contact_request = ContactRequest.objects.last()
        self.assertEqual(contact_request.sender, data['sender'])

    def test_contact_plugin2_empty_data_submission(self):
        """
        Test for plugin from https://github.com/maccesch/cmsplugin-contact
        :return:
        """
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'CustomContactPlugin', 'en', custom_label='contact us')
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)
        self.assertEqual(response.data['content'][0], 'This field is required.')
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], 'This field is required.')

    def test_contact_plugin2_data_submission(self):
        """
        Test for plugin from https://github.com/maccesch/cmsplugin-contact
        :return:
        """
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'CustomContactPlugin', 'en', form_name='contact us')
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'content': 'message text',
            'subject': 'message subject',
            'email': 'sender@example.com'
        }
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(mail.outbox), 1, )
        self.assertEqual(mail.outbox[0].extra_headers['Reply-To'], data['email'])
        self.assertEqual(mail.outbox[0].subject, '[contact us] ' + data['subject'])
        self.assertIn(data['content'], mail.outbox[0].body)

    def test_contact_plugin3_data_submission(self):
        """
        Test for plugin from https://github.com/maccesch/cmsplugin-contact
        :return:
        """
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'ContactPlugin', 'en', form_name='contact us')
        url = reverse('api:plugin-submit-data', kwargs={'pk': plugin.id})
        data = {
            'content': 'message text',
            'subject': 'message subject',
            'email': 'sender@example.com'
        }
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].extra_headers['Reply-To'], data['email'])
        self.assertEqual(mail.outbox[0].subject, '[contact us] ' + data['subject'])
        self.assertIn(data['content'], mail.outbox[0].body)
