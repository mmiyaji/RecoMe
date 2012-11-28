#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by mmiyaji on 2012-07-16.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import sys
import os

from django.contrib import admin
from rakuten.models import *

class AuthorAdmin(admin.ModelAdmin):
    pass

# モデルをadminサイトに表示させる
admin.site.register(History, AuthorAdmin)
admin.site.register(Parameter, AuthorAdmin)
admin.site.register(Individual, AuthorAdmin)

def main():
    pass

if __name__ == '__main__':
    main()
