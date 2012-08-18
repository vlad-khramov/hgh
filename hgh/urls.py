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
    url(r'^rating/$', 'apps.main.views.rating', name='rating'),
    url(r'^profile/$', 'apps.main.views.profile', name='profile'),

    url(r'^info/(?P<login>[^/]+)/$', 'apps.main.views.info', name='info'),


    url(r'', include('social_auth.urls')),
)
