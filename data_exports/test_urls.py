try:
    from django.conf.urls.defaults import patterns, url, include
except ImportError:  # django 1.6 and above
    from django.conf.urls import patterns, url, include
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^exports/', include('data_exports.urls', namespace='data_exports')),
)
