"""a2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from UI.dashboard import views
from UI.dashboard.views import UserLogin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^common/', include('UI.dashboard.urls')),
    url(r'^nodes/', include('UI.node.urls')),
    url(r'^pods/', include('UI.pod.urls')),
    url(r'^application/', include('UI.application.urls')),
    url(r'^topology/', include('UI.topology.urls')),
    url(r'^registry/', include('UI.registry.urls')),
    url(r'^deployment/', include('UI.deployment.urls')),
    url(r'^hpa/', include('UI.hpa.urls')),
    url(r'^systemconfig/', include('systemconfig.urls')),
    url(r'^$', UserLogin.as_view()),
    url(r'^get_all_ns/$', views.get_all_ns)

]
