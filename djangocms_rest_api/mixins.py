# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


class RESTPluginMixin(object):
    """
    fields and methods we might need to add to plugin
    maybe it would be a good idea to add fields to plugin model so we cn query only serializable plugins
    and users will have ability to configure parameters from site
    maybe we can add this to CMS Plugin, not sure we need it
    """
    accessible_by_rest = True
    permission_classes = None
    data_serializer_class = None

    # TODO: decide if we ned this method and a whole mixin too
    def process_data(self, request, instance, serializer):
        """

        :param instance: plugin instance
        :param request: django Request
        :param serializer: form or serializer class
        :return:
        """
        raise NotImplementedError
