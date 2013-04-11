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
    url(r'categories/id/(?P<id_category>(\d+))/products/matching/?$', views.CategoryMatching.as_view()),

    # Products
    url(r'product/new/?', views.NewProducts.as_view()),
    url(r'product/reference/(?P<reference>(\d+))/?$', views.Product.as_view()),
    url(r'product/reference/(?P<reference>(\d+))/recommendations/?$', views.ProductRecommendation.as_view()),

    # Cart
    url(r'cart/?$', views.CartAPIView.as_view()),
    url(r'cart/product/(?P<reference>(\d+))(/quantity/(?P<quantity>(\d+)))?/?$', views.CartManagementAPIView.as_view()),
)