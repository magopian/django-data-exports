#!/usr/bin/env python
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CsvExportConfig(AppConfig):
    name = 'data_exports'
    default_auto_field = "django.db.models.AutoField"
