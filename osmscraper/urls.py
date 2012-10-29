from django.conf.urls import patterns, include, url

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

    # Dalliz website
    url(r'^/?', 'dalliz.views.index'),

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
)
