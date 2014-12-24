from django.conf import settings
from django.conf.urls import patterns, include, url, static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'delayRepay.views.login', name='login'),
    url(r'^admin/', include(admin.site.urls)),

    #Authentication
    url(r'^login/$', 'delayRepay.views.login', name='login'),
    url(r'^auth/$', 'delayRepay.views.auth_view', name='auth_view'),
    url(r'^logout/$', 'delayRepay.views.logout', name='logout'),
    url(r'^addJourney/$', 'delayRepay.views.addJourney', name='addJourney'),
    url(r'^addTicket/$', 'delayRepay.views.addTicket', name='addTicket'),
    url(r'^loggedin/$', 'delayRepay.views.loggedin', name='loggedin'),
    url(r'^invalid/$', 'delayRepay.views.invalid_login', name='invalid_login'),

    url(r'^register/$', 'delayRepay.views.register_user', name='invalid_login'),
    url(r'^register_success/$', 'delayRepay.views.register_success', name='invalid_login'),


) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
