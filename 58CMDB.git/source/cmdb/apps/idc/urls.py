from django.conf.urls import patterns, include, url
import views
import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('idc.api',
    url(r'^(?i)api/idc/(?P<action>\w+)/$', csrf_exempt(api.Idc.as_view())),
    url(r'^(?i)api/upload/idc/(?P<action>\w+)/$', csrf_exempt(api.Upload.as_view())),
)

urlpatterns += patterns('idc.views',
    url(r'^(?i)idc/$', views.Idc.as_view(), name='idc.index'),
    url(r'^(?i)rack/$', views.Rack.as_view(), name='rack.index'),
    url(r'^(?i)position/$', views.Position.as_view(), name='position.index'),
    )
