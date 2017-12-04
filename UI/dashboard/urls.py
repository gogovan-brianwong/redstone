from django.conf.urls import url
from UI.dashboard.views import UserLogin, UserManagement
from . import views
urlpatterns = [
    url(r'^login/$', UserLogin.as_view()),
    url(r'^logout/$',UserManagement.as_view()),
    # url(r'^demo/', views.demo),
    # url(r'^dashboard/resources/$', views.get_resources),
    # url(r'^dashboard/cpu_metrics/$', views.show_cpu_metrics),
    # url(r'^dashboard/mem_metrics/$', views.show_mem_metrics),
    # url(r'^dashboard/fs_metrics/$', views.show_fs_metrics),
    # url(r'^dashboard/top_restart_pod/$', views.show_toprestart_pod),
    # url(r'^dashboard/alertbox/$', views.push_alert),
    # url(r'^dashboard/get_ttl_msg/$', views.get_current_ttl_msg),
    # url(r'^dashboard/get_login_user', views.get_login_user),
    # url(r'^dashboard/get_all_ns', views.getAllNamespaces),
    url(r'^dashboard/$', views.dashboard ),
    url(r'^$', UserLogin.as_view())

]

