#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')

version = get_version('djangocms_rest_api', '__init__.py')

setup(
    name='djangocms-rest-api',
    version=version,
    packages=['djangocms_rest_api', ],
    description='API for django cms.',
    long_description=open('README.rst').read(),
    author='SteelKiwi Development, Divio',
    author_email='getmansky@steelkiwi.com',
    include_package_data=True,
    install_requires=[
        'djangorestframework==3.4.0',
    ],
    license='MIT',
    url='https://github.com/divio/djangocms-rest-api',
    keywords='djangocms-rest-api',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ])
