from django.contrib import admin
from django.conf.urls import url, include

from UI.application import views
urlpatterns = [

    url(r'^index/(\w+)/$', views.AppIndexPorter.as_view()),
    url(r'^index/$', views.AppIndexPorter.as_view()),
    url(r'^details/(\d+)/$', views.AppDetailsPorter.as_view()),
    url(r'^listresources/$', views.listSCResources),
    url(r'^list/$', views.listNamespacedSecret),
    url(r'^all_deployed_app/$', views.allDeployedApp),
    url(r'^fetch_apptype/$', views.fetchApptype),
    url(r'^delete_app/$', views.deleteApp),
    url(r'^search_app/$', views.searchApp),
    url(r'^fetch_spec_app/([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)/$', views.fetchSpecificApp),

]