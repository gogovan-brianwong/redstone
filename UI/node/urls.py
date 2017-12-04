from django.conf.urls import url, include
from nodes import views, addhost, delhost
from UI.node.views import HostDetailsPorter, HostManagePorter, deletehost


urlpatterns = [


    url(r'^index/', HostDetailsPorter.as_view()),
    url(r'^details/([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)/$', HostDetailsPorter.as_view()),
    url(r'^update/([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)/$', HostManagePorter.as_view()),
    url(r'^addhost/auth/hostname/$', views.check_hostname),
    url(r'^addhost/auth/hostip/$', views.check_ipaddr),
    url(r'^addhost/$', addhost.addhost),
    # url(r'^delhost.html/(?P<nid>\w+)/',delhost.deletehost),
    url(r'^delhost.html/',deletehost)
    # url(r'^addhost.html/1/$', addhost.push_notification),
    # url(r'^deletehost/(?P<nid>\w+)/', views.deletehost),


]