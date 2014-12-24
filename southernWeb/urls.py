from django.conf import settings
from django.conf.urls import patterns, include, url, static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'delayRepay.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),

    #Authentication
    url(r'^accounts/$', 'delayRepay.views.login', name='login'),
    url(r'^accounts/login/$', 'delayRepay.views.login', name='login'),
    url(r'^accounts/auth/$', 'delayRepay.views.auth_view', name='auth_view'),
    url(r'^accounts/logout/$', 'delayRepay.views.logout', name='logout'),
    url(r'^accounts/addJourney/$', 'delayRepay.views.addJourney', name='addJourney'),
    url(r'^accounts/addTicket/$', 'delayRepay.views.addTicket', name='addTicket'),
    url(r'^accounts/loggedin/$', 'delayRepay.views.loggedin', name='loggedin'),
    url(r'^accounts/invalid/$', 'delayRepay.views.invalid_login', name='invalid_login'),

    url(r'^accounts/register/$', 'delayRepay.views.register_user', name='invalid_login'),
    url(r'^accounts/register_success/$', 'delayRepay.views.register_success', name='invalid_login'),


) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
