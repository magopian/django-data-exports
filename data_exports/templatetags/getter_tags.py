#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

from data_exports.compat import text_type


register = template.Library()


@register.filter()
def getattribute(model, item):
    """Chained lookup of item on model

    If item has dots (eg: 'foo.bar.baz'), recursively call getattribute():
    e = getattr(model, 'foo')
    e = getattr(e, 'bar')
    e = getattr(e, 'baz')
    At each step, check if e is a callable, and if so, use e()

    """
    elements = item.split('.')
    element = elements.pop(0)
    attr = getattr(model, element, None)
    if attr is None:  # end of recursion
        return
    if callable(attr):
        try:
            attr = attr()
        except:  # couldn't call this method without params
            return
    if elements:
        return getattribute(attr, '.'.join(elements))
    return attr  # no elements left (end of recursion)


@register.filter()
def getvalue(dictionary, item):
    """Equivalent to dict.get(item), provided for convenience"""
    return dictionary.get(item)


@register.filter()
def nice_display(item):
    """Display a comma-separated list of models for M2M fields"""
    if hasattr(item, 'all'):  # RelatedManager: display a list
        return ', '.join(map(text_type, item.all()))
    return item
