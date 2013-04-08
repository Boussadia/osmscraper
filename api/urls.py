#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.http import HttpResponse
from api import views

urlpatterns = patterns('',
	# Category
    url(r'categories/all/?$', views.CategoryAll.as_view()),
    url(r'categories/id/(?P<id_category>(\d+))/subs/?$', views.CategorySimple.as_view()),
    url(r'categories/id/(?P<id_category>(\d+))/products/(?P<key>all|top)/?$', views.CategoryProducts.as_view()),

    # Products
    url(r'product/reference/(?P<reference>(\d+))/?$', views.Product.as_view()),
    url(r'product/reference/(?P<reference>(\d+))/recomandations/?$', views.ProductRecomandation.as_view()),
)