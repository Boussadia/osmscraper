#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from api import views

import rest_framework

urlpatterns = patterns('',
    # Authentication
    url(r'auth/login/?$', views.UserAPI.as_view()),
    url(r'auth/logout/?$', views.UserAPI.as_view()),

	# Category
    url(r'categories/all/?$', views.CategoryAll.as_view()),
    url(r'categories/id/(?P<id_category>(\d+))/subs/?$', views.CategorySimple.as_view()),
    url(r'categories/id/(?P<id_category>(\d+))/(?P<type_fetched>products|promotions)/(?P<key>all|mid|end|top)/?$', (views.CategoryProducts.as_view())),
    url(r'categories/id/(?P<id_category>(\d+))/products/matching/?$', views.CategoryMatching.as_view()),

    # Products
    url(r'product/new/?', views.NewProducts.as_view()),
    url(r'product/reference/(?P<reference>(\d+))/?$', views.Product.as_view()),
    url(r'product/reference/(?P<reference>(\d+))/recommendations/?$', views.ProductRecommendation.as_view()),

    # Cart
    url(r'cart/?$', views.CartAPIView.as_view()),
    url(r'cart/product/(?P<reference>(\d+))(/quantity/(?P<quantity>(\d+)))?/?$', views.CartManagementAPIView.as_view()),

    # Osm
    url(r'osm/?$', views.OSMAPIView.as_view()),
)

urlpatterns += patterns('',
    url(r'Auth/', include('rest_framework.urls', namespace='rest_framework')),
)