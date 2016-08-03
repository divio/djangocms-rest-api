# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.test_utils.testcases import CMSTestCase
from rest_framework.test import APIClient


class CMSApiTestCase(CMSTestCase):
    client_class = APIClient
