from django.conf.urls import patterns, include, url
import views
import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('dpt.api',
#    url(r'^(?i)api/dpt/(?P<action>\w+)/(?P<id>\d+)/$', csrf_exempt(api.Dpt.as_view())),
#    url(r'^(?i)api/(?P<action>\w+)/$', csrf_exempt(api.Org.as_view())),
#    url(r'^(?i)api/dptopt/(?P<action>\w+)/$', csrf_exempt(api.Dpt.as_view())),
#    url(r'^(?i)api/orgdpt/(?P<action>\w+)/$', csrf_exempt(api.OrgDpt.as_view())),
#    url(r'^(?i)api/userbsp/(?P<action>\w+)/$', csrf_exempt(api.UserBsp.as_view())),
#    url(r'^(?i)api/dptuser/(?P<action>\w+)/$', csrf_exempt(api.DptUser.as_view())),
#    url(r'^(?i)api/clusteruser/(?P<action>\w+)/$', csrf_exempt(api.ClusterUser.as_view())),
    url(r'^(?i)api/busline/(?P<action>\w+)/$', csrf_exempt(api.BusLine.as_view())),
    url(r'^(?i)api/cluster/(?P<action>\w+)/$', csrf_exempt(api.Cluster.as_view())),
    url(r'^(?i)api/clusterserver/(?P<action>\w+)/$', csrf_exempt(api.ClusterServer.as_view())),
#    url(r'^(?i)api/buslineserver/(?P<action>\w+)/$', csrf_exempt(api.BuslineServer.as_view())),
#    url(r'^(?i)api/dpt/(?P<action>\w+)/$', csrf_exempt(api.Dpt.as_view())),
)

urlpatterns += patterns('org.views',
    url(r'^(?i)orgtree/$', views.OrgTree.as_view(), name="orgtree.index"),
)

urlpatterns += patterns('dpt.views',
    # url(r'^(?i)dpt/$', views.Dpt.as_view(), name="dpt.index"),
    # url(r'^(?i)dpt/detail/$', views.DptDetail.as_view(), name="dptdetail.index"),
    # url(r'^(?i)dpt/bsp/assoc/$', views.OrgTree.as_view(), name="dptbsp.index"),
    # url(r'^(?i)dpt/user/assoc/$',  views.DptUser.as_view(), name="dptuser.index"),
    # url(r'^(?i)dpt/pid/$',  views.DptLevel.as_view(), name="dptlevel.index"),
    url(r'^(?i)busline/$',  views.BusLine.as_view(), name="busline.index"),
    url(r'^(?i)busline/detail/$',  views.BusLineDetail.as_view(), name="buslinedetail.index"),
    # url(r'^(?i)busline/user/assoc/$',  views.BusLineUser.as_view(), name="buslineuser.index"),
    # url(r'^(?i)busline/dpt/assoc/$',  views.BusLineDpt.as_view(), name="buslinedpt.index"),
    url(r'^(?i)cluster/$', views.Cluster.as_view(), name="cluster.index"),
    url(r'^(?i)cluster/user/assoc/$', views.ClusterUser.as_view(), name="clusteruser.index"),
    # url(r'^(?i)cluster/busline/assoc/$', views.ClusterBusline.as_view(), name="clusterbusline.index"),
    # url(r'^(?i)busline/detail/$', views.BuslineDetail.as_view(), name="buslinedetail.index"),
)
