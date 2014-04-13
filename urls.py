from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fitched.views.home', name='home'),
    # url(r'^fitched/', include('fitched.foo.urls')),
    url(r'^$', 'alpha.views.index'),
    url(r'^register/', 'alpha.views.register'),
    url(r'^synced/', 'alpha.views.synced'),
    url(r'^syncedprogress/', 'alpha.views.syncedprogress'),
    (r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
