from django.conf.urls import patterns, url
from bo_apis.views import *

urlpatterns = patterns("",
	url(r'^news/?$', news , name='news'),
    url(r'^$', data , name='data'),
)

