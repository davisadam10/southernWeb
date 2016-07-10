"""
coding=utf-8
Urls used for the delay repay app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url, static
from rest_framework import routers
from django.contrib import admin
admin.autodiscover()

from delayRepayRest import views as restViews
router = routers.DefaultRouter()
router.register(r'rest/users', restViews.UserViewSet)



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
    url(r'^answerCaptcha/$', 'delayRepay.views.answerCaptcha', name='answerCaptcha'),
    url(r'^register/$', 'delayRepay.views.register_user', name='invalid_login'),
    url(r'^register_success/$', 'delayRepay.views.register_success', name='invalid_login'),
    url(r'^', include(router.urls)),
    url(r'^rest/user/$', restViews.UserView.as_view(), name='UserView'),
    url(r'^rest/friends/$', restViews.FriendsView.as_view(), name='FriendsView'),
    url(r'^rest/unclaimedDelays/$', restViews.UnclaimedDelaysView.as_view(), name='UnclaimedDelays'),
    url(r'^rest/journeys/$', restViews.JourneysView.as_view(), name='Journeys'),
    url(r'^rest/best_ticket/$', restViews.BestAvailableTicket.as_view(), name='BestTicket'),
    url(r'^rest/set_delay_claimed/$', restViews.SetDelayAsClaimed.as_view(), name='SetDelayClaimed'),




) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
