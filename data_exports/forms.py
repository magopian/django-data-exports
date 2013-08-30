#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from data_exports.models import Export, Column
from inspect_model import InspectModel


class ExportForm(forms.ModelForm):

    class Meta:
        model = Export

    def __init__(self, *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        if self.instance:  # don't allow modification of the model once created
            del self.fields['model']


class ColumnForm(forms.ModelForm):
    # make sure we have a select widget for the column choice
    # Choice list is computed in data_exports.admin.ColumnFormSet
    column = forms.ChoiceField(choices=[])

    class Meta:
        model = Column


class ColumnFormSet(forms.models.BaseInlineFormSet):

    def add_fields(self, form, index):
        """Filter the form's column choices

        This is done at the formset level as there's no other way i could find
        to get the parent object (stored in self.instance), and the form at the
        same time.

        """
        super(ColumnFormSet, self).add_fields(form, index)
        model = self.instance.model.model_class()
        choices = get_choices(model)
        form.fields['column'].choices = [(u'', '---------')] + choices


def get_choices(model, prefixes=[]):
    choices = []
    prefix = '.'.join(prefixes)
    if prefix:
        prefix = '%s.' % prefix
    im = InspectModel(model)
    items = ['%s%s' % (prefix, i) for i in im.items]
    choices += zip(items, items)
    for f in im.relation_fields:
        related_field = getattr(model, f)
        if hasattr(related_field, 'field'):  # ForeignKey
            related_model = related_field.field.rel.to
        else:
            related_model = related_field.related.model
        if f in prefixes:  # we already went through this model
            return []  # end of recursion
        new_prefixes = prefixes + [f]
        choices += get_choices(related_model, prefixes=new_prefixes)
    return choices
