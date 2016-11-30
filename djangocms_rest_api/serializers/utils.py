# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import inspect
from django.utils.translation import get_language_from_request


class RequestSerializer(object):
    @property
    def request(self):
        return self._context['request']

    @property
    def language(self):
        return get_language_from_request(self.request, check_path=True)
