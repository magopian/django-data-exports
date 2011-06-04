#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template


register = template.Library()

@register.filter()
def getattribute(model, item):
    return getattr(model, item)

@register.filter()
def getvalue(dictionary, item):
    return dictionary.get(item)

@register.filter()
def nice_display(item):
    if hasattr(item, 'all'): # RelatedManager, display a list
        return ', '.join(map(unicode, item.all()))
    return item

