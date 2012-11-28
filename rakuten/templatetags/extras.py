#!/usr/bin/env python
# encoding: utf-8
"""
cutword.py

Created by mmiyaji on 2012-11-27.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from django import template
register = template.Library()

@register.filter
def cutword(value, arg):
    return value[:int(arg)]
# register.filter('cutword', cutword)
