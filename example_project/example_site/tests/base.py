# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import with_statement

import os.path

from cms.api import create_page, add_plugin
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from filer.models import Image
from rest_framework import status
from rest_framework.test import APIClient

from plugins.models import Slide, ContactRequest
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

        image1 = SimpleUploadedFile("image.jpg", b"content")
        image2 = SimpleUploadedFile("image.jpg", b"content")
        slide_1 = Slide.objects.create(title='slide 1', image=image1, slider=instance)
        slide_2 = Slide.objects.create(title='slide 2', image=image2, slider=instance)
        url = reverse('api:plugin-detail', kwargs={'pk': plugin.id})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data['inlines']), 1)
        self.assertEqual(len(response.data['inlines']['slides']), 2)
        self.assertIn(slide_1.image.url, response.data['inlines']['slides'][0]['image'])

    def test_plugin_with_children(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        columns = add_plugin(placeholder, "MultiColumnPlugin", "en")
        column_1 = add_plugin(placeholder, "ColumnPlugin", "en", target=columns, width='10%')
        column_2 = add_plugin(placeholder, "ColumnPlugin", "en", target=columns, width='30%')
        text_plugin_1_1 = add_plugin(placeholder, "TextPlugin", "en", target=column_1, body="I'm the first")
        text_plugin_1_2 = add_plugin(placeholder, "TextPlugin", "en", target=column_1, body="I'm the second")
        text_plugin_2_1 = add_plugin(placeholder, "TextPlugin", "en", target=column_2, body="I'm the third")
        url = reverse('api:plugin-detail', kwargs={'pk': columns.id})
        response = self.client.get(url, format='json')
        data = response.data
        self.assertIn('children', data)
        self.assertEqual(len(data['children']), 2)
        self.assertEqual(len(data['children'][0]['children']), 2)
        self.assertEqual(data['children'][0]['children'][0]['body'], text_plugin_1_1.body)
        self.assertEqual(data['children'][0]['children'][1]['body'], text_plugin_1_2.body)
        self.assertEqual(len(data['children'][1]['children']), 1)
        self.assertEqual(data['children'][1]['children'][0]['body'], text_plugin_2_1.body)

    def test_plugin_with_children_with_inlines(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        columns = add_plugin(placeholder, "MultiColumnPlugin", "en")
        column_1 = add_plugin(placeholder, "ColumnPlugin", "en", target=columns, width='10%')
        column_2 = add_plugin(placeholder, "ColumnPlugin", "en", target=columns, width='30%')
        column_3 = add_plugin(placeholder, "ColumnPlugin", "en", target=columns, width='60%')
        text_plugin_1_1 = add_plugin(placeholder, "TextPlugin", "en", target=column_1, body="I'm the first")
        text_plugin_1_2 = add_plugin(placeholder, "TextPlugin", "en", target=column_1, body="I'm the second")
        text_plugin_2_1 = add_plugin(placeholder, "TextPlugin", "en", target=column_2, body="I'm the third")

        plugin = add_plugin(placeholder, 'SliderWithInlinesPlugin', 'en', target=column_3, name='Slider')
        instance, plugin_model = plugin.get_plugin_instance()

        image1 = SimpleUploadedFile("image.jpg", b"content")
        image2 = SimpleUploadedFile("image.jpg", b"content")
        slide_1 = Slide.objects.create(title='slide 1', image=image1, slider=instance)
        slide_2 = Slide.objects.create(title='slide 2', image=image2, slider=instance)

        url = reverse('api:plugin-detail', kwargs={'pk': columns.id})
        response = self.client.get(url, format='json')
        data = response.data
        self.assertIn('children', data)
        self.assertEqual(len(data['children']), 3)
        self.assertEqual(len(data['children'][0]['children']), 2)
        self.assertEqual(data['children'][0]['children'][0]['body'], text_plugin_1_1.body)
        self.assertEqual(data['children'][0]['children'][1]['body'], text_plugin_1_2.body)
        self.assertEqual(len(data['children'][1]['children']), 1)
        self.assertEqual(data['children'][1]['children'][0]['body'], text_plugin_2_1.body)
        self.assertIn('inlines', data['children'][2]['children'][0])
        self.assertIn('slides', data['children'][2]['children'][0]['inlines'])
        self.assertEqual(len(data['children'][2]['children'][0]['inlines']['slides']), 2)

    def test_plugin_mapping(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        image = Image.objects.create(file=SimpleUploadedFile("image.jpg", b"content"))
        plugin = add_plugin(placeholder, "FilerImagePlugin", "en", image=image)
        url = reverse('api:plugin-detail', kwargs={'pk': plugin.id})
        response = self.client.get(url, format='json')
        data = response.data
        self.assertIsNotNone(data['plugin_data']['image'])
        self.assertTrue(isinstance(data['plugin_data']['image'], dict))
        # TODO: check urls
        self.assertIn(image.url, data['plugin_data']['image']['file'])

    def test_custom_serializer_list(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'SliderPlugin', 'en', name='Slider')
        instance, plugin_model = plugin.get_plugin_instance()

        image = SimpleUploadedFile("image.jpg", b"content")
        image = SimpleUploadedFile("image.jpg", b"content")
        slide_1 = Slide.objects.create(title='slide 1', image=image, slider=instance)
        slide_2 = Slide.objects.create(title='slide 2', image=image, slider=instance)
        url = reverse('api:plugin-list')
        response = self.client.get(url, format='json')
        self.assertIn('test', response.data[0])

    def test_custom_serializer_detail(self):
        page = create_page('page', 'page.html', 'en', published=True)
        placeholder = page.placeholders.get(slot='content')
        plugin = add_plugin(placeholder, 'SliderPlugin', 'en', name='Slider')
        instance, plugin_model = plugin.get_plugin_instance()

        image = SimpleUploadedFile("image.jpg", b"content")
        image = SimpleUploadedFile("image.jpg", b"content")
        slide_1 = Slide.objects.create(title='slide 1', image=image, slider=instance)
        slide_2 = Slide.objects.create(title='slide 2', image=image, slider=instance)
        url = reverse('api:plugin-detail', kwargs={'pk': plugin.id})
        response = self.client.get(url, format='json')
        self.assertIn('test', response.data)
