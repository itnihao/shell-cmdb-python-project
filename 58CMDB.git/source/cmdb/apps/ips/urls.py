from django.conf.urls import patterns, include, url
import views
import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('ips.api',
    url(r'^(?i)api/ip/(?P<action>\w+)/$', csrf_exempt(api.Ip.as_view())),
    url(r'^(?i)api/upload/ip/(?P<action>\w+)/$', csrf_exempt(api.Upload.as_view())),
)

urlpatterns += patterns('ips.views',
        url(r'^(?i)ips/$', views.Ips.as_view(), name='ips.index'),
)

