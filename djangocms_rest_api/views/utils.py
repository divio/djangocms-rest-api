# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.cms_menus import get_visible_pages
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone


class QuerysetMixin(object):

    def get_queryset(self):
        site = get_current_site(self.request)
        queryset = super(QuerysetMixin, self).get_queryset()
        if self.request.user.is_staff:
            return queryset.drafts().on_site(site=site).distinct()
        else:
            return queryset.public().on_site(site=site).distinct()


def check_if_page_is_visible(request, page, site=None):
    # used next check for now, think of replacement later
    pages = get_visible_pages(request, [page, ], site=site)

    page_is_visible = page.id in pages

    if page_is_visible and not (not request.user.is_staff and (
            (page.publication_date <= timezone.now() or page.publication_date is None) and (
                page.publication_end_date >= timezone.now() or page.publication_end_date is None)
    )):
        return False

    return page_is_visible
