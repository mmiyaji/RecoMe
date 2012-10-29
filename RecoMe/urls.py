from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^(/)?', include('rakuten.urls')),
                       url(r'^404/$', 'RecoMe.views.status404', name='404'),
                       )
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            (r'^media/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
                            (r'^admin/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.ADMIN_MEDIA_PREFIX}),
                            )
