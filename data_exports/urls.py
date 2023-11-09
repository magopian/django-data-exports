#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from data_exports import views


urlpatterns = [
    url(r'^add$', views.export_add, name='export_add'),
    url(r'^(?P<slug>[^/]+)$', views.export_view, name='export_view'),
    url(r'^(?P<slug>[^/]+)/columns$', views.export_cols, name='export_cols'),
]
