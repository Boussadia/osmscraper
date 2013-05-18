#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
# from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic import TemplateView, RedirectView

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

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Include api urls
    url(r'^api/', include('api.urls')),

    # Include mturk urls
    url(r'^mturk/', include('mturk.urls')),

     # Include dev frontend urls
    url(r'^comparateur/', include('frontend.urls')),

    # Tags creator app
    url(r'^backend/tags/(?P<id_category>(\d+))(/(?P<tags>(.+)))?/?$', 'tags.views.tags'),
    url(r'^backend/tags/autocomplete/?$', 'tags.views.autocomplete'),
    url(r'^backend/tags/?$', 'tags.views.index'),

    # Dalliz backend categories builder
    url(r'^backend/categorie/?$', 'categories_builder.views.index'),
    url(r'^backend/categorie/delete/(?P<id>(\d+))/?$', 'categories_builder.views.delete_category'),
    url(r'^backend/categorie/id/(?P<id>(\d+))/position/(?P<position>(\d+))/?$', 'categories_builder.views.change_position'),
    url(r'^backend/categorie/id/(?P<id>(\d+))/name/?$', 'categories_builder.views.change_name'),
    url(r'^backend/categorie/((?P<parent_url>(.+))/)?(?P<url>(.+))/?$', 'categories_builder.views.sub_categories'),

    # Dalliz brands builder
    url(r'^backend/brand/?$', 'brand_builder.views.index'),
    url(r'^backend/brand/delete/(?P<id>(\d+))/?$', 'brand_builder.views.delete_brand'),
    url(r'^backend/brand/(?P<id>(\d+))/?$', 'brand_builder.views.sub_brands'),

    # Dalliz backend categories matcher app
    url(r'^backend/categories_matcher/?$', 'categories_matcher.views.index'),
    url(r'^backend/categories_matcher/(?P<osm>(\w)+)/(?P<level>\d+)(/(?P<parent>\d+))?/?$', 'categories_matcher.views.categories'),
    url(r'^backend/categories_matcher/add_link/?$', 'categories_matcher.views.add_link'),
    url(r'^backend/categories_matcher/delete_link/?$', 'categories_matcher.views.delete_link'),
    url(r'^backend/categories_matcher/get_links/(?P<osm>(\w)+)/(?P<category_id>\d+)/?$', 'categories_matcher.views.get_links'),

    # Brand matcher
    url(r'^backend/matcher/(?P<osm>(\w)+)/brand/(?P<id>\d+)/?$','brand_matcher.views.selector'),
    url(r'^backend/matcher/(?P<osm>(\w)+)/brand/cancel/(?P<id>\d+)/?$', 'brand_matcher.views.cancel'),
    url(r'^backend/matcher/brand/autocomplete/?$', 'brand_matcher.views.autocomplete'),
    url(r'^backend/matcher/(?P<osm>(\w)+)/brand/set/(?P<osm_brand_id>\d+)/(?P<dalliz_brand_id>\d+)/?$', 'brand_matcher.views.set'),

    # Product tags cleaner
    url(r'^backend/matcher/(?P<osm>(\w)+)/tags/(?P<category_id>\d+)/?$','matcher.views.category'),
    url(r'^backend/matcher/(?P<osm>(\w)+)/tags/set/(?P<product_id>\d+)/(?P<tags>(.+))/?$','matcher.views.tags'),
    url(r'^backend/matcher/(?P<osm>(\w)+)/tags/match/(?P<osm_from>(\w)+)/(?P<product_id_to>\d+)/(?P<product_id_from>\d+)/?$','matcher.views.set_match'),
    # url(r'^backend/matcher/(?P<osm>(\w)+)/tags/nomatch/(?P<product_id>\d+)/?$','matcher.views.set_no_match'),
    url(r'^backend/matcher/(?P<osm>(\w)+)/tags/nosimilarity/(?P<osm_from>(\w)+)/(?P<product_id_to>\d+)/(?P<product_id_from>\d+)/?$','matcher.views.set_no_similarity'),
    url(r'^backend/matcher/(?P<osm>(\w)+)/tags/categorie/set/(?P<product_id>\d+)/?$','matcher.views.set_categories'),
    url(r'^backend/matcher/tags/categorie/autocomplete/?$','matcher.views.autocomplete_category'),
    url(r'^backend/matcher/(?P<osm>(\w)+)/tags/comment/(?P<product_id>\d+)/?$','matcher.views.comment'),


    # Dalliz website
    url(r'^/?$', 'dalliz.views.index'),
    # url(r'^prospects/?$','dalliz.views.prospects'),
    url(r'^a-propos-de-dalliz/?$', 'dalliz.views.a_propos'),
    url(r'^mentions-legales/?$','dalliz.views.mentions'),
    url(r'^partenariat/?$', 'dalliz.views.partenariat'),
    url(r'^conditions-generale-d-utilisation/?$','dalliz.views.cgu'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='dalliz/robots.txt') ),
    url(r'^google0b72a6d52b859293\.html$', TemplateView.as_view(template_name='dalliz/google0b72a6d52b859293.html') ),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='dalliz/sitemap.xml') ),
    
    url(r'^.*$', RedirectView.as_view(url='/')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'cachebuster.views.static_serve', {'document_root': settings.STATIC_ROOT,}),
        url(r'^media/(?P<path>.*)$', 'cachebuster.views.media_serve', {'document_root': settings.MEDIA_ROOT,}),
    )
