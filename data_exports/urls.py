#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from django.conf.urls.defaults import patterns, url
except ImportError:  # django 1.6 and above
    from django.conf.urls import patterns, url
from data_exports import views


urlpatterns = patterns(
    '',
    url(r'^add$', views.export_add, name='export_add'),
    url(r'^(?P<slug>[^/]+)$', views.export_view, name='export_view'),
    url(r'^(?P<slug>[^/]+)/columns$', views.export_cols, name='export_cols'),
)
