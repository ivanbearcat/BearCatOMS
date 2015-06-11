from django.conf.urls import patterns, include, url
from login.views import login,login_auth
from main.views import main

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BearCatOMS.views.home', name='home'),
    # url(r'^BearCatOMS/', include('BearCatOMS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login),
    url(r'^login_auth/', login_auth),
    url(r'^main/', main),
)
