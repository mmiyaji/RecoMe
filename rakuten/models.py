#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by mmiyaji on 2012-11-29.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *
from django.db import models
# Create your models here.
from django.db.models import Q
from django.core.cache import cache
from django.contrib.auth import models as auth_models

class History(models.Model):
    user = models.ForeignKey(auth_models.User, db_index=True)
    content_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    def get_by_user(self, user):
        return History.objects.order_by('-created_at').filter(isvalid=True).filter(user=user)
    def __unicode__(self):
        return self.content_id
class Parameter(models.Model):
    word = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    score = models.FloatField(default=0.0, blank=True, null=True, db_index=True)
    rank = models.IntegerField(default=0, blank=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    def __unicode__(self):
        return "%s(%s) %s" % (self.word,str(self.score),str(self.rank))
class Individual(models.Model):
    user = models.ForeignKey(auth_models.User, db_index=True)
    parameter = models.ManyToManyField(Parameter, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    recent_history = models.ForeignKey(History, db_index=True)
    @staticmethod
    def get_by_user(user):
        return Individual.objects.order_by('-created_at').filter(isvalid=True).filter(user=user)
    def __unicode__(self):
        p = u"%s: " % self.user.username
        for i in self.parameter.all():
            p += u"%s(%s), " % (i.word,str(i.score))
        return p
