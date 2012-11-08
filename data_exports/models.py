#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Format(models.Model):
    name = models.CharField(max_length=50)
    file_ext = models.CharField(max_length=10, blank=True)
    mime = models.CharField(max_length=50)
    template = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Export(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    model = models.ForeignKey(ContentType)
    export_format = models.ForeignKey(
        Format,
        blank=True,
        null=True,
        help_text=_(u"Leave empty to display as HTML"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('data_exports:export_view', kwargs={'slug': self.slug})

    def get_export_link(self):
        if self.slug:
            return '<a href="%s">Download</a>' % self.get_absolute_url()
        else:
            return _('Export not ready')
    get_export_link.allow_tags = True


class Column(models.Model):
    export = models.ForeignKey(Export)
    column = models.CharField(max_length=255)
    label = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.column
