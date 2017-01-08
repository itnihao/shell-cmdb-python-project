from django.conf.urls import url
from django.contrib import admin
from example_t import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$',views.Index.as_view(),name="model"),
    url(r'^pool$',  views.Pool.as_view(),name='pool'),
]