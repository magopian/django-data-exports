#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.test import TestCase
from data_exports.models import Format, Export, Column
from data_exports.forms import ColumnForm, ColumnFormSet
from inspect_model import InspectModel


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

    def test_column_choices(self):
        ColumnInlineFormSet = inlineformset_factory(Export,
                                                    Column,
                                                    form=ColumnForm,
                                                    formset=ColumnFormSet)
        formset = ColumnInlineFormSet(instance=self.empty_export)
        # the column field has choices
        form = formset.forms[0]
        self.assertTrue(hasattr(form.fields['column'], 'choices'))
        # all the table items are in the column field choices
        choices = form.fields['column'].choices
        self.assertTrue(all([(i, i) in choices for i in self.im.items]))

    def test_export_html(self):
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

    def test_export_csv(self):
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
                '_save': 'Save',
                })
        print resp
        # when creating, "save" is equivalent to "save and continue editing"
        self.assertRedirects(resp,
                             reverse('admin:data_exports_export_change',
                                     args=[1])) # first export created, id=1

        # once an export is created, it's no more possible to modify its model
        resp = self.client.get(reverse('admin:data_exports_export_change',
                                       args=[1]))
        self.assertContains(resp, 'name="export_format"')
        self.assertNotContains(resp, 'name="model"')
