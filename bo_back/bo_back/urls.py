from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin
admin.autodiscover()
from bo_report.views import Moderation
from bo_report.views import websiteGenerator, report

urlpatterns = patterns('',
    url(r"^blocked/", include("bo_report.urls")),   
    url(r'^admin/moderate/$', Moderation.as_view(), name='moderation_page'),
    url(r'^admin/moderate/(?P<country_code>\w+)/(?P<choose_opt>\w+)/$', Moderation.as_view(), name='moderation_page'),
    url(r'^admin/moderate/(?P<country_code>\w+)/$', Moderation.as_view(), name='moderation_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ping/?$', include('ping.urls')),
    url(r'^load/?$', websiteGenerator, name='loadfromhome'),
    url(r'^report/?$', report, name='loadfromhome'),
    url(r'^.*$', RedirectView.as_view(url='http://www.blockedonline.com', permanent=False), name='index')
)