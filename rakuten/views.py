#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by mmiyaji on 2012-10-29.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
import os, re, sys, commands, time, datetime, random, logging
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from rakuten.models import *
from django.utils.encoding import force_unicode, smart_str
from django.core import serializers
from django.conf import settings
from django.http import Http404
from django.core.cache import cache
from django.contrib.sessions.backends.db import SessionStore
import simplejson
from django.core import serializers
import networkx as nx
import numpy
logger = logging.getLogger('app')

def main():
    pass

if __name__ == '__main__':
    main()
