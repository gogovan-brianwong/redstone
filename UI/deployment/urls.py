from django.conf.urls import url

from . import views
from .views import DeploymentDetails,DeploymentIndex

urlpatterns = [
    url(r'^index/$', DeploymentIndex.as_view()),
    url(r'^details/([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)/$', DeploymentDetails.as_view()),
    url(r'^adddeploy/$', views.adddeploy)

]