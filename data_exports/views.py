#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView
from data_exports.forms import ExportForm, ColumnForm, ColumnFormSet
from data_exports.models import Export, Column


class ExportView(DetailView):
    model = Export

    def get_context_data(self, **kwargs):
        context = super(ExportView, self).get_context_data(**kwargs)
        model = self.object.model.model_class()
        context['data'] = model.objects.all()
        return context

    def render_to_response(self, context, **kwargs):
        resp = super(ExportView, self).render_to_response(context, **kwargs)
        export_format = self.object.export_format
        if export_format:
            filename = '%s.%s' % (self.object.slug, export_format.file_ext)
            resp['Content-Type'] = export_format.mime
            resp['Content-Disposition'] = 'attachment; filename=%s' % filename
        return resp

    def get_template_names(self, **kwargs):
        template_names = super(ExportView, self).get_template_names(**kwargs)
        export_format = self.object.export_format
        if export_format:
            template_names.insert(0, export_format.template)
        return template_names
export_view = login_required(ExportView.as_view())


class ExportAdd(CreateView):
    model = Export

    def get_success_url(self):
        return reverse('data_exports:export_cols',
                       kwargs={'slug': self.object.slug})
export_add = login_required(ExportAdd.as_view())


class ExportCols(UpdateView):
    column_inline = inlineformset_factory(Export,
                                          Column,
                                          form=ColumnForm,
                                          formset=ColumnFormSet)
    form_class = ExportForm
    model = Export
    template_name = 'data_exports/export_cols.html'

    def get_context_data(self, **kwargs):
        context = super(ExportCols, self).get_context_data(**kwargs)
        context['formset'] = self.column_inline(instance=self.object)
        if hasattr(self, 'formset'):  # formset was POSTed, but is invalid
            context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            formset = self.column_inline(request.POST, instance=self.object)
            if formset.is_valid():
                formset.save()
                return self.form_valid(form)
            else:
                self.formset = formset
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)
export_cols = login_required(ExportCols.as_view())
