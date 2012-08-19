# coding: utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hgh.views.home', name='home'),
    # url(r'^hgh/', include('hgh.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'apps.main.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='logout'),

    url(r'^$', 'apps.main.views.home', name='home'),
    url(r'^rating/experience/$', 'apps.main.views.rating', {'type':'experience'}, name='rating_exp'),
    url(r'^rating/power/$', 'apps.main.views.rating', {'type':'power'}, name='rating_pow'),
    url(r'^profile/$', 'apps.main.views.profile', name='profile'),

    url(r'^fight/$', 'apps.main.views.prebattle', name='prebattle'),
    url(r'^battle/$', 'apps.main.views.battle', name='battle'),
    url(r'^battleresult/$', 'apps.main.views.postbattle', name='postbattle'),

    url(r'^battleinfo/(?P<id>\d+)/$', 'apps.main.views.battle_info', name='battle_info'),

    url(r'^info/(?P<login>[^/]+)/$', 'apps.main.views.info', name='info'),


    url(r'', include('social_auth.urls')),
)
