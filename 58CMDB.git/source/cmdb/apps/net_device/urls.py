from django.conf.urls import patterns, include, url
import views
import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('net_device.api',
#    url(r'^(?i)api/netdevice/(?P<action>\w+)/(?P<id>\d+)/$', api.NetDevice.as_view()),
#    url(r'^(?i)api/netdevice/(?P<action>\w+)/$', csrf_exempt(api.NetDevice.as_view())),
#    url(r'^(?i)api/idcmodule/(?P<action>\w+)/(?P<id>\d+)/$', api.IdcModule.as_view()),
#    url(r'^(?i)api/idcmodule/(?P<action>\w+)/$', csrf_exempt(api.IdcModule.as_view())),
#    url(r'^(?i)api/nicport/(?P<action>\w+)/(?P<id>\d+)/$', api.NicPort.as_view()),
#    url(r'^(?i)api/nicport/(?P<action>\w+)/$', csrf_exempt(api.NicPort.as_view())),
#    url(r'^(?i)api/nicportlink/(?P<action>\w+)/(?P<id>\d+)/$', api.NicPortLink.as_view()),
#    url(r'^(?i)api/nicportlink/(?P<action>\w+)/$', csrf_exempt(api.NicPortLink.as_view())),
)

urlpatterns += patterns('net_device.views',
        url(r'^(?i)netdevice/$', views.NetDevice.as_view(), name='netdevice.index'),
)
