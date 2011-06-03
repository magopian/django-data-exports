#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from data_exports.models import Column


class ColumnForm(forms.ModelForm):
    # make sure we have a select widget for the column choice
    # Choice list is computed in data_exports.admin.ColumnFormSet
    column = forms.ChoiceField(choices=[])

    class Meta:
        model = Column

