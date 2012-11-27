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

urlpatterns = patterns('',
                       url(r'^$', 'rakuten.general.home', name='home'),
                       url(r'^content/$', 'rakuten.content.home'),
                       url(r'^login/$', 'rakuten.general.signin'),
                       url(r'^logout/$', 'rakuten.general.signout'),
                       )
