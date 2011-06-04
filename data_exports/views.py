#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from data_exports.models import Export


class ExportView(DetailView):
    model = Export
    template_object_name = 'export'

    def get_context_data(self, **kwargs):
        context = super(ExportView, self).get_context_data(**kwargs)
        model = self.object.model.model_class()
        context['data'] = model.objects.all()
        return context

    def render_to_response(self, context, **kwargs):
        resp = super(ExportView, self).render_to_response(context, **kwargs)
        export_format = self.object.export_format
        if export_format:
            filename = '%s.%s' % (self.object.slug, export_format.name)
            resp['Content-Type'] = export_format.mime
            resp['Content-Disposition'] = 'attachment; filename=%s' % filename
        return resp

    def get_template_names(self, **kwargs):
        template_names = super(ExportView, self).get_template_names(**kwargs)
        export_format = self.object.export_format
        if export_format:
            template_names.insert(0, export_format.template)
        return template_names

export_view = ExportView.as_view()
