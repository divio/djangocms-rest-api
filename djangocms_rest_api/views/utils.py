# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.cms_menus import get_visible_pages
from cms.models import Page
from cms.utils.page_resolver import get_page_queryset
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


def check_if_page_is_visible(request, page, pages=None, site=None):
    # used next check for now, think of replacement later

    if page.login_required and not request.user.is_authenticated():
        return False
    if not pages:
        if request.user.is_staff:
            pages = Page.objects.all()
        else:
            pages = Page.objects.public()
        pages = pages.filter(id=page.pk)

    if not pages:
        return False

    pages = get_visible_pages(request, pages, site=site)
    page_is_visible = page.id in pages

    if page_is_visible and not (request.user.is_staff or (
            (page.publication_date is None or page.publication_date <= timezone.now()) and (
                            page.publication_end_date is None or page.publication_end_date >= timezone.now())
    )):
        return False

    return page_is_visible
