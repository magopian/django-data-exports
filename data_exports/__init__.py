#!/usr/bin/env python
# -*- coding: utf-8 -*-

pkg_resources = __import__('pkg_resources')
distribution = pkg_resources.get_distribution('django-data-exports')

__version__ = distribution.version
