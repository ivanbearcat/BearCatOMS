from django.conf.urls import patterns, include, url
from login.views import login,login_auth,logout,not_login
from main.views import main
from monitor.views import nagios,zabbix
from user_manage.views import chpasswd,post_chpasswd
from assets.views import assets_asset,assets_asset_data,assets_asset_save

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
    url(r'^logout/', logout),
    url(r'^accounts/login/$',not_login),
    url(r'^main/', main),
    url(r'^nagios/', nagios),
    url(r'^zabbix/', zabbix),
    url(r'^chpasswd/', chpasswd),
    url(r'^post_chpasswd/', post_chpasswd),
    url(r'^assets_asset/', assets_asset),
    url(r'^assets_asset_data/', assets_asset_data),
    url(r'^assets_asset_save/', assets_asset_save),
)
