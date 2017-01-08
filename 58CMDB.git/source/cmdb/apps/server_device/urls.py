from django.conf.urls import patterns, include, url
import views
import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('server_device.api',
        url(r'^(?i)api/Server/(?P<action>\w+)/$', csrf_exempt(api.Server.as_view())),
        url(r'^(?i)api/Logger/(?P<action>\w+)/$', csrf_exempt(api.Logger.as_view())),
        url(r'^(?i)api/upload/server/(?P<action>\w+)/$', csrf_exempt(api.Upload.as_view())),
)

urlpatterns += patterns('server_device.views',
        url(r'^$', views.Index.as_view(), name='home'),
        url(r'^(?i)server/$', views.Server.as_view(), name='server.index'),
       # url(r'^(?i)assignserver/$', csrf_exempt(views.AssignServer.as_view()), name='assign.server.index'),
        url(r'^(?i)repairs/$', views.Repairs.as_view(), name='repairs.index'),
        url(r'^(?i)repairorderform/$', views.RepairOrderForm.as_view(), name='repairsorderform.index'),
        url(r'^(?i)pool/$', views.RresourcePool.as_view(), name='RresourcePool.index'),
        url(r'^(?i)poolmanagment/$', views.PoolManagment.as_view(), name='PoolManagment.index'),
        url(r'^(?i)baseresource/$', views.BaseResource.as_view(), name='baseresource.index'),
)
