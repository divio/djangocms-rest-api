# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import with_statement

import os.path

from cms.api import create_page, add_plugin
from django.core.cache import cache
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient

from plugins.models import Slide
from tests.utils import CMSApiTestCase


class PagesTestCase(CMSApiTestCase):
    client_class = APIClient

    def tearDown(self):
        cache.clear()

    def test_page_list_unauthorised(self):
        """
        Test that anonymous user and access public pages via API
        """
        user = self.get_superuser()
        title_1 = 'page'
        title_2 = 'inner'
        title_3 = 'page 3'
        page = create_page(title_1, 'page.html', 'en', published=True)
        page_2 = create_page(title_2, 'page.html', 'en', published=True, parent=page)
        page_3 = create_page(title_3, 'page.html', 'en', published=False)

        url = reverse('api:page-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)
        for page in response.data:
            self.assertIn(page.get('title'), {title_1, title_2})

    def test_page_list_admin(self):
        """
        Test that admin user and access all pages via API
        """
        user = self.get_superuser()
        title_1 = 'page'
        title_2 = 'inner'
        title_3 = 'page 3'
        page = create_page(title_1, 'page.html', 'en', published=True)
        page_2 = create_page(title_2, 'page.html', 'en', published=True, parent=page)
        page_3 = create_page(title_3, 'page.html', 'en', published=False)

        with self.login_user_context(user):
            url = reverse('api:page-list')
            response = self.client.get(url, format='json')
            self.assertEqual(len(response.data), 3)
            for page in response.data:
                self.assertIn(page.get('title'), {title_1, title_2, title_3})


class PlaceHolderTestCase(CMSApiTestCase):

    def test_placeholders(self):
        """
        Test that placeholder are accessible and contains required info
        """
        page = create_page('page', 'page.html', 'en', published=True)
        url = reverse('api:placeholder-list')
        response = self.client.get(url, formst='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['slot'], 'content')
        page2 = create_page('page2', 'feature.html', 'en', published=True)
        response = self.client.get(url, formst='json')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[1]['slot'], 'feature')
        self.assertEqual(response.data[2]['slot'], 'content')


class PluginTestCase(CMSApiTestCase):

    def test_plugins_list(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin_1 = add_plugin(placeholder, 'TextPlugin', 'en', body='Test content')
        plugin_2 = add_plugin(placeholder, 'TextPlugin', 'en', body='Test content 2')
        url = reverse('api:plugin-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['plugin_data']['body'], plugin_1.body)
        self.assertEqual(response.data[1]['plugin_data']['body'], plugin_2.body)

    def test_plugin_detail(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin_1 = add_plugin(
            placeholder, 'GoogleMapPlugin', 'en', address="Riedtlistrasse 16", zipcode="8006", city="Zurich", )
        url = reverse('api:plugin-detail', kwargs={'pk': plugin_1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.data['plugin_type'], 'GoogleMapPlugin')
        self.assertEqual(response.data['plugin_data']['address'], plugin_1.address)

    def test_plugin_with_inlines(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'SliderWithInlinesPlugin', 'en', name='Slider')
        instance, plugin_model = plugin.get_plugin_instance()
        from django.core.files.uploadedfile import SimpleUploadedFile
        image_path = os.path.join(os.path.dirname(__file__), 'test-image.jpg')
        image1 = SimpleUploadedFile(
            name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        image2 = SimpleUploadedFile(
            name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        slide_1 = Slide.objects.create(title='slide 1', image=image1, slider=instance)
        slide_2 = Slide.objects.create(title='slide 2', image=image2, slider=instance)
        url = reverse('api:plugin-detail', kwargs={'pk': plugin.id})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['inlines']), 1)
        self.assertEqual(len(response.data['inlines']['slides']), 2)
        self.assertEqual(response.data['inlines']['slides'][0]['image'], slide_1.image.url)

