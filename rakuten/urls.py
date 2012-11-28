#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by mmiyaji on 2012-10-29.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'rakuten.general.home', name='home'),
                       url(r'^content/$', 'rakuten.content.home'),
                       url(r'^content/(?P<genre_id>\w+)/$', 'rakuten.content.home'),
                       url(r'^genre/$', 'rakuten.content.genre'),
                       url(r'^genre/(?P<genre_id>\w+)/$', 'rakuten.content.genre'),
                       url(r'^recommend/$', 'rakuten.content.home', {'name':'recommend'}),
                       url(r'^recommend/(?P<content_id>[\w:]+)/$', 'rakuten.content.home', {'name':'recommend'}),
                       url(r'^login/$', 'rakuten.general.signin'),
                       url(r'^logout/$', 'rakuten.general.signout'),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^adminsite/', include(admin.site.urls)),
                       )
