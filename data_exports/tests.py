#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import IntegrityError, models
from django.forms.models import inlineformset_factory
from django.test import TestCase
from data_exports.templatetags import getter_tags as ttags
from data_exports.models import Format, Export, Column
from data_exports.forms import ColumnForm, ColumnFormSet, get_choices
from inspect_model import InspectModel

from data_exports.compat import text_type


class ExportTest(TestCase):

    def setUp(self):
        # create an export of the Export model (inception !)
        ct = ContentType.objects.get(app_label='data_exports', model='export')
        self.empty_export = Export.objects.create(name='test empty export',
                                                  slug='test-empty-export',
                                                  model=ct)
        self.im = InspectModel(Export)

        # create an export of the Export model with columns
        self.export = Export.objects.create(name='test export',
                                            slug='test-export',
                                            model=ct)
        for f in self.im.items:
            Column.objects.create(export=self.export,
                                  column=f,
                                  order=0)

        user = User.objects.create_user('admin', 'admin@admin.com', 'admin')
        user.is_superuser = True
        user.save()

    def test_slug(self):
        """Make sure the slug is unique."""
        with self.assertRaisesRegexp(IntegrityError,
                                     "column slug is not unique"):
            Export.objects.create(name='foo',
                                  slug=self.empty_export.slug,
                                  model=self.empty_export.model)

    def test_column_choices(self):
        """Choices computed for the exported model

        When using the ColumnFormSet and the ColumnForm, all the accessible
        items (fields, relations, methods, attributes...) from the exported
        model are present in the "column" form field choices

        """
        class OneToOneToExport(models.Model):
            """Fake model.

            Make sure that get_choices works with
            SingleRelatedObjectDescriptor, as explained in ticket #4.

            """
            name = models.CharField(max_length=50)
            o2o = models.OneToOneField(Export)

        # reload the model's relations, to have the OneToOneToExport's relation
        # taken into account
        self.empty_export._meta._fill_related_objects_cache()
        self.empty_export._meta.init_name_map()

        ColumnInlineFormSet = inlineformset_factory(Export,
                                                    Column,
                                                    form=ColumnForm,
                                                    formset=ColumnFormSet)
        formset = ColumnInlineFormSet(instance=self.empty_export)
        # the column field has choices
        form = formset.forms[0]
        self.assertTrue(hasattr(form.fields['column'], 'choices'))
        choices = form.fields['column'].choices
        # all the model items are in the column field choices
        self.assertTrue(all([(i, i) in choices for i in self.im.items]))
        # and all the related model items are in the fields choices
        # export has a FK to Format named 'export_format'
        im_format = ['export_format.%s' % i
                     for i in InspectModel(Format).items]
        self.assertTrue(all([(i, i) in choices for i in im_format]))
        # export has a FK to ContentType named 'model'
        im_ct = ['model.%s' % i for i in InspectModel(ContentType).items]
        self.assertTrue(all([(i, i) in choices for i in im_ct]))
        # OneToOneToExport has a OneToOneField to ContentType named
        # 'onetoonetoexport'
        im_o2o = ['onetoonetoexport.%s' % i
                  for i in InspectModel(OneToOneToExport).items]
        self.assertTrue(all([(i, i) in choices for i in im_o2o]))
        # revert changes to name_map:  'unload' the OneToOneToExport relation
        del self.empty_export._meta._name_map['onetoonetoexport']

    def test_export_without_format(self):
        """Export without a format renders to a simple template"""
        self.client.login(username='admin', password='admin')
        # empty export
        resp = self.client.get(reverse('data_exports:export_view',
                               kwargs={'slug': self.empty_export.slug}))
        self.assertContains(resp, 'No columns where defined')
        # full export
        resp = self.client.get(reverse('data_exports:export_view',
                               kwargs={'slug': self.export.slug}))
        self.assertNotContains(resp, 'No columns where defined')
        for c in self.export.column_set.all():
            self.assertContains(resp, c.label if c.label else c)

    def test_export_with_format(self):
        """Export with a format gives a file download"""
        # create a format for a "naive csv export"
        csv_format = Format.objects.create(
            name='naive csv',
            file_ext='csv',
            mime='text/csv',
            template='data_exports/export_detail_csv.html')

        self.client.login(username='admin', password='admin')

        self.export.export_format = csv_format
        self.export.save()
        resp = self.client.get(reverse('data_exports:export_view',
                                       kwargs={'slug': self.export.slug}))
        self.assertEqual(resp['Content-Type'], self.export.export_format.mime)
        self.assertEqual(resp['Content-Disposition'],
                         'attachment; filename=%s.%s' % (
                             self.export.slug,
                             self.export.export_format.file_ext))

    def test_export_templatetag(self):
        """Templatetags provided for convenience"""
        # getattribute
        self.assertEqual(ttags.getattribute(self.export, 'model'),
                         getattr(self.export, 'model'))
        # getvalue
        d = {'foo': 'bar'}
        self.assertEqual(ttags.getvalue(d, 'foo'), d.get('foo'))
        # nice_display: displays a list for FK and ManyToMany
        column_list = ttags.nice_display(self.export.column_set).split(', ')
        for c in self.export.column_set.all():
            self.assertTrue(text_type(c) in column_list)
        # make sure getattribute and nice_display work on all choices
        for c, name in get_choices(Export):
            e = ttags.getattribute(self.export, c)
            ttags.nice_display(e)


class AdminTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('admin', 'admin@admin.com', 'admin')
        user.is_staff = True
        user.is_superuser = True
        user.save()

    def test_create_export(self):
        self.client.login(username='admin', password='admin')
        ct = ContentType.objects.get(app_label='data_exports', model='export')
        resp = self.client.post(reverse('admin:data_exports_export_add'), {
            'name': 'test export',
            'slug': 'test-export',
            'model': ct.pk,
            '_save': 'Save'})
        # when creating, "save" is equivalent to "save and continue editing"
        self.assertRedirects(resp,
                             reverse('admin:data_exports_export_change',
                                     args=[1]))  # first export created, id=1

        # once an export is created, it's no more possible to modify its model
        resp = self.client.get(reverse('admin:data_exports_export_change',
                                       args=[1]))
        self.assertContains(resp, 'name="export_format"')
        self.assertNotContains(resp, 'name="model"')
