from django.conf.urls import url

from UI.pod import views

urlpatterns = [


    url(r'^status/', views.PodStatusPorter.as_view()),
    url(r'^details/([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)/$', views.PodStatusPorter.as_view()),


]