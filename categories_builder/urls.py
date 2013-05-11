#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'/?$', 'categories_builder.views.index'),
    url(r'delete/(?P<id>(\d+))/?$', 'categories_builder.views.delete_category'),
    url(r'id/(?P<id>(\d+))/position/(?P<position>(\d+))/?$', 'categories_builder.views.change_position'),
    url(r'id/(?P<id>(\d+))/name/(?P<new_name>(.+))/?$', 'categories_builder.views.change_name'),
    url(r'((?P<parent_url>(.+))/)?(?P<url>(.+))/?$', 'categories_builder.views.sub_categories'),
)

