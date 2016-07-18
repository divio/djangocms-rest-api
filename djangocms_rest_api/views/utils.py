# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.sites.shortcuts import get_current_site


class QuerysetMixin(object):

    def get_queryset(self):
        site = get_current_site(self.request)
        queryset = super(QuerysetMixin, self).get_queryset()
        if self.request.user.is_staff:
            return queryset.drafts().on_site(site=site).distinct()
        else:
            return queryset.public().on_site(site=site).distinct()
