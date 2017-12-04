from django.conf.urls import url

from UI.topology import views

urlpatterns = [

    url(r'^index/', views.index),




]