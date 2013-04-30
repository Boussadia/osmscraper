#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from api import views

urlpatterns = patterns('',
	# Category
    url(r'categories/all/?$', cache_page(60 * 60 *24)(views.CategoryAll.as_view())),
    url(r'categories/id/(?P<id_category>(\d+))/subs/?$', cache_page(60 * 60 *24)(views.CategorySimple.as_view())),
    url(r'categories/id/(?P<id_category>(\d+))/products/(?P<key>all|mid|end|top)/?$', (views.CategoryProducts.as_view())),
    url(r'categories/id/(?P<id_category>(\d+))/products/matching/?$', cache_page(60 * 60 *24)(views.CategoryMatching.as_view())),

    # Products
    url(r'product/new/?', cache_page(60 * 60 *24)(views.NewProducts.as_view())),
    url(r'product/reference/(?P<reference>(\d+))/?$', cache_page(60 * 60 *24)(views.Product.as_view())),
    url(r'product/reference/(?P<reference>(\d+))/recommendations/?$', cache_page(60 * 60 *24)(views.ProductRecommendation.as_view())),

    # Cart
    url(r'cart/?$', views.CartAPIView.as_view()),
    url(r'cart/product/(?P<reference>(\d+))(/quantity/(?P<quantity>(\d+)))?/?$', views.CartManagementAPIView.as_view()),
)