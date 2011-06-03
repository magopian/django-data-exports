#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter()
def getattribute(model, item):
    return getattr(model, item)

@register.filter()
def getvalue(dictionary, item):
    return dictionary.get(item)
