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
    url(r'categories/all/?$', cache_page(60 * 60 * 24)(views.CategoryAll.as_view())),
    url(r'categories/id/(?P<id_category>(\d+))/subs/?$', cache_page(60 * 60 * 24)(views.CategorySimple.as_view())),
    url(r'categories/id/(?P<id_category>(\d+))/(?P<type_fetched>products|promotions)/(?P<key>all|mid|end|top)/?$', cache_page(60 * 60 * 24)(views.CategoryProducts.as_view())),
    url(r'categories/id/(?P<id_category>(\d+))/products/matching/?$', cache_page(60 * 60 * 24)(views.CategoryMatching.as_view())),

    # Products
    url(r'product/new/?', cache_page(60 * 60 * 24)(views.NewProducts.as_view())),
    url(r'product/reference/(?P<reference>(\d+))/?$', cache_page(60 * 60 * 24)(views.Product.as_view())),
    url(r'product/reference/(?P<reference>(\d+))/recommendations/?$', cache_page(60 * 60 * 24)(views.ProductRecommendation.as_view())),

    # Cart
    url(r'cart/?$', views.CartAPIView.as_view()),
    url(r'cart/product/(?P<reference>(\d+))(/quantity/(?P<quantity>(\d+)))?/?$', views.CartAPIView.as_view()),
    url(r'cart/importation/?$', views.CartImportation.as_view()),

    # Osm
    url(r'osm/?$', views.OSMSAPIView.as_view()),
)

urlpatterns += patterns('',
    url(r'Auth/', include('rest_framework.urls', namespace='rest_framework')),
)