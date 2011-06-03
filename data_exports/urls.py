#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from data_exports import views


urlpatterns = patterns('',
    url(r'^(?P<slug>[^/]+)$', views.export_view, name='export_view'),
)
