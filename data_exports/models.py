#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Format(models.Model):
    name = models.CharField(max_length=50)
    mime = models.CharField(max_length=50)
    attachment = models.BooleanField(default=True)
    template = models.CharField(max_length=255)


    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Export(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    display_labels = models.BooleanField(default=True)
    model = models.ForeignKey(ContentType)
    export_format = models.ForeignKey(Format, blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('data_exports:export_view', [], {'slug': self.slug})


class Column(models.Model):
    export = models.ForeignKey(Export)
    column = models.CharField(max_length=255)
    label = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.column
