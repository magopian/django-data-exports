#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from data_exports.models import Export, Column
from inspect_model import InspectModel

#####################################################################
# Monkey Patch Inspect Model
def update_fields(self):
    self.fields = set()
    self.relation_fields = set()
    self.many_fields = set()
    opts = getattr(self.model, '_meta', None)
    if opts:
        for field in opts.get_fields():
            direct = not field.auto_created or field.concrete
        if not direct:  # relation or many field from another model
            name = field.get_accessor_name()
            field = field.field
            if field.rel.multiple:  # m2m or fk to this model
                self._add_item(name, self.many_fields)
            else:  # one to one
                self._add_item(name, self.relation_fields)
        else:  # relation, many or field from this model
            name = field.name
            if field.related_model:  # relation or many field
                if field.many_to_many:  # m2m
                    self._add_item(name, self.many_fields)
                else:
                    self._add_item(name, self.relation_fields)
            else:  # standard field
                self._add_item(name, self.fields)
        try:
            from django.contrib.contenttypes.generic import (
                GenericForeignKey)
            for f in opts.virtual_fields:
                if isinstance(f, GenericForeignKey):
                    self._add_item(f.name, self.relation_fields)
        except ImportError:
            pass


InspectModel.update_fields = update_fields
######################################################################


class ExportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        if self.instance:  # don't allow modification of the model once created
            del self.fields['model']

    class Meta:
        model = Export
        exclude = ()


class ColumnForm(forms.ModelForm):
    # make sure we have a select widget for the column choice
    # Choice list is computed in data_exports.admin.ColumnFormSet
    column = forms.ChoiceField(choices=[])

    class Meta:
        model = Column
        exclude = ()


class ColumnFormSet(forms.models.BaseInlineFormSet):
    def get_choices(self):
        # avoid multiple choices generation for django 1.6+
        if not hasattr(self, "_choices"):
            model = self.instance.model.model_class()
            self._choices = [(u'', '---------')] + get_choices(model)
        return self._choices

    def add_fields(self, form, index):
        """Filter the form's column choices

        This is done at the formset level as there's no other way i could find
        to get the parent object (stored in self.instance), and the form at the
        same time.

        """
        super(ColumnFormSet, self).add_fields(form, index)
        form.fields['column'].choices = self.get_choices()


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
            related_model = related_field.field.related_model
        else:
            related_model = related_field.related.model
        if f in prefixes:  # we already went through this model
            return []  # end of recursion
        new_prefixes = prefixes + [f]
        choices += get_choices(related_model, prefixes=new_prefixes)
    return choices
