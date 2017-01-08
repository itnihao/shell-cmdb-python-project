from django.conf.urls import patterns, include, url
import views
import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('auth.view',
    url(r'^(?i)api/Auth/token/$', views.Auth.as_view()),
    url(r'^(?i)api/Auth/(?P<action>\w+)/$', csrf_exempt(api.Permission.as_view())),
    )

urlpatterns += patterns('server_device.views',
    url(r'^(?i)usermanager/$', views.UserManager.as_view(), name='usermanager.index'),
    url(r'^(?i)usergroupmanager/$', views.UserGroupManager.as_view(), name='usergroupmanager.index'),
    url(r'^(?i)rolemanager/$', views.RoleManager.as_view(), name='rolemanager.index'),
    url(r'^(?i)logout/$', views.LogOut.as_view(), name='logout.index'),
)
