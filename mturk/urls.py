#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.http import HttpResponse
from api import views

urlpatterns = patterns('',
    url(r'key/(?P<key>(.+))/?$', 'mturk.views.index'),
)