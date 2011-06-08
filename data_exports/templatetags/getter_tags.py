#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template


register = template.Library()

@register.filter()
def getattribute(model, item):
    """Equivalent to getattr(model, item)

    If item has dots (eg: foo.bar.baz), recursively call getattribute():
    e = getattr(model, 'foo')
    e = getattr(e, 'bar')
    e = getattr(e, 'baz')
    Then return e, or e() if it's a callable

    """
    elements = item.split('.')
    element = elements.pop(0)
    attr = getattr(model, element, None)
    if attr is None: # end of recursion
        return attr
    if not elements: # no elements left (end of recursion)
        if callable(attr):
            try:
                return attr()
            except: # couldn't call this method without params after all
                return ''
        return attr
    return getattribute(attr, '.'.join(elements))

@register.filter()
def getvalue(dictionary, item):
    """Equivalent to dict.get(item), provided for convenience"""
    return dictionary.get(item)

@register.filter()
def nice_display(item):
    """Display a comma-separated list of models for M2M fields"""
    if hasattr(item, 'all'): # RelatedManager: display a list
        return ', '.join(map(unicode, item.all()))
    return item
