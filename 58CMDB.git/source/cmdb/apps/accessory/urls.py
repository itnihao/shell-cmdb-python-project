from django.conf.urls import patterns, include, url
import views
import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('accessory.api',
     url(r'^(?i)api/upload/accessory/(?P<action>\w+)/$', csrf_exempt(api.Upload.as_view())),
)

urlpatterns += patterns('accessory.views',
        url(r'^(?i)accessory/$', views.Accessory.as_view(), name='accessory.index'),
)
