"""
coding=utf-8
Urls used for the delay repay app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url, static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'delayRepay.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),

    # Authentication
    url(r'^login/$', 'delayRepay.views.login', name='login'),
    url(r'^logout/$', 'delayRepay.views.logout', name='logout'),
    url(r'^addJourney/$', 'delayRepay.views.addJourney', name='addJourney'),
    url(r'^addTicket/$', 'delayRepay.views.addTicket', name='addTicket'),
    url(r'^addFriend/$', 'delayRepay.views.addFriend', name='addFriend'),
    url(r'^unclaimedDelays/$', 'delayRepay.views.unclaimedDelays', name='unclaimedDelays'),
    url(r'^noTicket/$', 'delayRepay.views.noTicket', name='noTicket'),
    url(r'^register/$', 'delayRepay.views.register_user', name='invalid_login'),
    url(r'^register_success/$', 'delayRepay.views.register_success', name='invalid_login'),



) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
