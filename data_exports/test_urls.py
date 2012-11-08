from django.conf.urls import patterns, url, include
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^np_admin/', include(admin.site.urls)),
    url(r'^exports/', include('data_exports.urls', namespace='data_exports')),
)
