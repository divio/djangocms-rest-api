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


class ClassLookupDict(object):
    def __init__(self, mapping):
        self.mapping = mapping

    def get_base_class(self, key):
        if hasattr(key, '_proxy_class'):
            base_class = key._proxy_class
        else:
            base_class = key
        return base_class

    def get_cls(self, key):
        base_class = self.get_base_class(key=key)

        for cls in inspect.getmro(base_class):
            if cls in self.mapping:
                return self.mapping[cls]

    def __getitem__(self, key):
        cls = self.get_cls(key=key)
        if cls is not None:
            return cls
        base_class = self.get_base_class(key=key)
        raise KeyError('Class %s not found in lookup.' % base_class.__name__)

    def __setitem__(self, key, value):
        self.mapping[key] = value

    def get(self, key, default=None):
        cls = self.get_cls(key=key)
        if cls is not None:
            return cls
        return default
