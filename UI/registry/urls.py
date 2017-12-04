from django.contrib import admin
from django.conf.urls import url, include
from UI.registry.views import RegistryLogin, RegistryInfo

urlpatterns = [

    url(r'^login/$', RegistryLogin.as_view()),
    url(r'^index/$', RegistryInfo.as_view()),
    # url(r'^info/(?P<uid>\w+)/', views.image_info),
    # url(r'^remove/(\d+)/', views.remove_image),
]