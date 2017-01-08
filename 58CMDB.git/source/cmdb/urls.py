from django.conf.urls import patterns, include, url
from apps.accessory import urls as accessory_url
from apps.server_device import urls as server_url
from apps.net_device import urls as net_url
from apps.dpt import urls as dpt_url
from apps.ips import urls as ips_url
from apps.idc import urls as idc_url
from apps.auth import urls as auth_url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cmdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += server_url.urlpatterns
urlpatterns += accessory_url.urlpatterns
urlpatterns += net_url.urlpatterns
urlpatterns += idc_url.urlpatterns
urlpatterns += ips_url.urlpatterns
urlpatterns += dpt_url.urlpatterns
urlpatterns += auth_url.urlpatterns
