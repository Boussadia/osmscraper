#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.http import HttpResponse

urlpatterns = patterns('',
    url(r'.*/?$', 'frontend.views.index'),
)