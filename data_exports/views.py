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
        mimetype = 'text/html'
        export_format = self.object.export_format
        if export_format:
            mimetype = export_format.mime
        resp = super(ExportView, self).render_to_response(
                context,
                content_type=mimetype,
                **kwargs)
        if export_format and export_format.attachment:
            filename = '%s.%s' % (self.object.slug, export_format.name)
            resp['Content-Disposition'] = 'attachment; filename=%s' % filename
        return resp

    def get_template_names(self, **kwargs):
        template_names = super(ExportView, self).get_template_names(**kwargs)
        export_format = self.object.export_format
        if export_format:
            return [export_format.template]
        return template_names

export_view = ExportView.as_view()
