#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'osmscraper.views.home', name='home'),
    # url(r'^osmscraper/', include('osmscraper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Categories matcher app
    url(r'^categories_matcher/?$', 'categories_matcher.views.index'),
    url(r'^categories_matcher/(?P<osm>(\w)+)/(?P<level>\d+)(/(?P<parent>\d+))?/?$', 'categories_matcher.views.categories'),
    url(r'^categories_matcher/add_link/?$', 'categories_matcher.views.add_link'),
    url(r'^categories_matcher/delete_link/?$', 'categories_matcher.views.delete_link'),
    url(r'^categories_matcher/get_links/(?P<osm>(\w)+)/(?P<category_id>\d+)/?$', 'categories_matcher.views.get_links'),

    # Telemarket/Monoprix products validation
    url(r'^telemarket_monoprix/products/?$', 'telemarket_monoprix.views.index'),
    url(r'^telemarket_monoprix/products/suggestions/(?P<id>\d+)/?$', 'telemarket_monoprix.views.suggestions'),
    url(r'^telemarket_monoprix/products/next/(?P<id>\d+)/?$', 'telemarket_monoprix.views.next'),
    url(r'^telemarket_monoprix/products/previous/(?P<id>\d+)/?$', 'telemarket_monoprix.views.previous'),
    url(r'^telemarket_monoprix/products/cancel/(?P<id>\d+)/?$', 'telemarket_monoprix.views.cancel'),


    # Dalliz website
    url(r'^/?$', 'dalliz.views.index'),
    url(r'^a-propos-de-dalliz/?$', 'dalliz.views.a_propos'),
    url(r'^partenariat/?$', 'dalliz.views.partenariat'),
    url(r'^produit/(?P<name>((\w)+-?)+)/?$','dalliz.views.product'),
    url(r'^categorie/(?P<sub_category>((\w)+-?)+)/?$','dalliz.views.category'),
    url(r'^panier/?$','dalliz.views.cart'),
    url(r'^add/cart/?$','dalliz.views.add_to_cart'),
    url(r'^remove/cart/?$','dalliz.views.remove_from_cart'),
    url(r'^conditions-generale-d-utilisation$','dalliz.views.cgu'),
    url(r'^mentions-legales/$','dalliz.views.mentions'),
    url(r'^login/?$','dalliz.views.login'),
    url(r'^logout/?$','dalliz.views.logout'),
    url(r'^compte/?$','dalliz.views.account'),
    url(r'^robots\.txt$', direct_to_template, {'template': 'dalliz/robots.txt', 'mimetype': 'text/plain'})
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'cachebuster.views.static_serve', {'document_root': settings.STATIC_ROOT,}),
        url(r'^media/(?P<path>.*)$', 'cachebuster.views.media_serve', {'document_root': settings.MEDIA_ROOT,}),
    )