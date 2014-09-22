from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='homepage.html')),
	url(r'^getinvolved/?$', TemplateView.as_view(template_name='getinvolved.html')),
	url(r'^explore/?$', TemplateView.as_view(template_name='explore.html')),
	url(r'^about/?$', TemplateView.as_view(template_name='about.html')),
	url(r'^data/', include("bo_apis.urls")),
	url(r'^ping/?$', include('ping.urls')),
)
