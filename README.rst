**Deprecated**

This project is no longer supported.

Divio will undertake no further development or maintenance of this project. If you are interested in continuing to develop it, use the fork functionality from GitHub. We are not able to transfer ownership of the repository to another party.

Please have a look at alternatives such as `djangocms-spa <https://github.com/dreipol/djangocms-spa>`_.

===================
djangocms-rest-api
===================

An application to use CMS content and features via REST API.

djangocms-rest-api uses Django REST framework to serve django CMS data through a REST API

Installation
------------

* pip install djangocms-rest-api
* Edit ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'djangocms_rest_api',
        ...
    ]

* Edit ``urls.py``::

    urlpatterns = [
        ...
        url(r'^api/', include('djangocms_rest_api.urls', namespace='api')),
        ...
    ]

* That's all!


Features
--------


Credits
-------


License
-------

MIT
