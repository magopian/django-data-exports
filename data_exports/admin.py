#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django
from django.contrib import admin
from data_exports.models import Export, Column, Format
from data_exports.forms import ColumnForm, ColumnFormSet


POST_URL_CONTINUE = None
if django.get_version() < '1.6':
    POST_URL_CONTINUE = '../%s/'


class ColumnInline(admin.TabularInline):
    extra = 0
    form = ColumnForm
    formset = ColumnFormSet
    model = Column


class ExportAdmin(admin.ModelAdmin):
    inlines = [ColumnInline]
    list_display = ['name', 'slug', 'model', 'export_format',
                    'get_export_link']
    list_filter = ['export_format', 'model']
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['model']
    search_fields = ['name', 'slug', 'model']

    def get_readonly_fields(self, request, obj=None):
        """The model can't be changed once the export is created"""
        if obj is None:
            return []
        return super(ExportAdmin, self).get_readonly_fields(request, obj)

    def get_formsets(self, request, obj=None):
        if obj is None:
            return
        if not hasattr(self, 'inline_instances'):
            self.inline_instances = self.get_inline_instances(request)
        for inline in self.inline_instances:
            yield inline.get_formset(request, obj)

    def response_add(self, request, obj, post_url_continue=POST_URL_CONTINUE):
        """If we're adding, save must be "save and continue editing"

        Two exceptions to that workflow:
        * The user has pressed the 'Save and add another' button
        * We are adding a user in a popup

        """
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(ExportAdmin, self).response_add(request,
                                                     obj,
                                                     post_url_continue)

admin.site.register(Export, ExportAdmin)
admin.site.register(Format)
