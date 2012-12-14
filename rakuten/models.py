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
if settings.MONGODB_USE:
    import pymongo

class Parameter(models.Model):
    word = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    score = models.FloatField(default=0.0, blank=True, null=True, db_index=True)
    rank = models.IntegerField(default=0, blank=True, null=True, db_index=True)
    path = models.TextField(default="", blank=True, null=True) # word01(0.212),word02(0.23),..
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    isdeleted_path = models.BooleanField(default=False, db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    def clone(self):
        p = Parameter()
        p.word = self.word
        p.score = self.score
        p.rank = self.rank
        p.path = self.path
        p.save()
        return p
    def hscore(self):
        return str(self.score)[:4]
    def get_path_as_html(self):
        return self.path.replace(",",",<br />")
    def path_length(self):
        return len(self.path.split(","))-1
    def __unicode__(self):
        return "%s(%s) %s // %s" % (self.word,str(self.score),str(self.rank),self.path)
class Individual(models.Model):
    parameter = models.ManyToManyField(Parameter, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    # recent_history = models.ForeignKey(History, db_index=True)
    def sorted_param(self):
        return sorted(self.parameter.all(), key=lambda x: x.score, reverse=True)
    def clone(self):
        i = Individual()
        i.save()
        for p in self.parameter.all():
            i.parameter.add(p.clone())
        i.save()
        return i
    def __unicode__(self):
        p = u""
        for i in self.parameter.all():
            p += u"%s(%s), " % (i.word,str(i.score))
        return p
class History(models.Model):
    user = models.ForeignKey(auth_models.User, db_index=True)
    individual = models.ManyToManyField(Individual, blank=True, null=True)
    content_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    def get_content(self):
        conn = pymongo.Connection(settings.MONGODB_PATH, settings.MONGODB_PORT)
        db = conn.rakuten
        usedb = db.booktree
        return usedb.find_one({'id':self.content_id})
    @staticmethod
    def get_by_user(user):
        return History.objects.order_by('-created_at').filter(isvalid=True).filter(user=user)
    def __unicode__(self):
        return u"%s: %s" % (self.user.username,self.created_at)
