#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from data_exports.models import Export, Column, Format
from data_exports.forms import ColumnForm
from django.forms.models import BaseInlineFormSet
from inspect_model import InspectModel


class ColumnFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        """Filter the form's column choices

        This is done at the formset level as there's no other way i could find
        to get the parent object (stored in self.instance), and the form at the
        same time.

        """
        super(ColumnFormSet, self).add_fields(form, index)
        model = self.instance.model.model_class()
        im = InspectModel(model)
        columns = [(i, i) for i in im.items]
        form.fields['column'].choices = columns


class ColumnInline(admin.TabularInline):
    extra = 0
    form = ColumnForm
    formset = ColumnFormSet
    model = Column


class ExportAdmin(admin.ModelAdmin):
    inlines = [ColumnInline]
    list_display = ['name', 'slug', 'model', 'export_format']
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
        for inline in self.inline_instances:
            yield inline.get_formset(request, obj)

    def response_add(self, request, obj, post_url_continue='../%s/'):
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
