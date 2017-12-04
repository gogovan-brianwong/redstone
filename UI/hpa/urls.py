from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^addhpa/$', views.add_hpa),
    url(r'^selectns/$', views.select_ns),
    url(r'^showall/$', views.show_all),
    url(r'^removehpa/$', views.remove_hpa),
    url(r'^getresources/$', views.getresources),
    url(r'^alertbox/$', views.alertbox),
    url(r'^tableupdate/$', views.tableupdate),


]
