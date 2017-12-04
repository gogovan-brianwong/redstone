from django.contrib import admin
from django.conf.urls import url, include

from . import views
urlpatterns = [

    url(r'^index/$', views.SystemInfo.as_view()),
    url(r'^apiserver/manifest/$', views.SystemAPIServer.as_view()),

]