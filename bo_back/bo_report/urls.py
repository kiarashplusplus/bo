from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from bo_report.views import *
from django.http import HttpResponse
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r'^news/?$', news , name='news'),
    url(r'^report/?$', report , name='report'),
    url(r'^load/?$', websiteGenerator , name='load'),
    url(r'^software_version.html/?$', lambda r: HttpResponse("1.1.0")),
    url(r'^.*$', RedirectView.as_view(url='http://www.blockedonline.com', permanent=False), name='index')
)

