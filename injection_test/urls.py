__author__ = 'Elliot'

from django.views.generic.base import RedirectView
from django.contrib.auth.views import password_change, logout, login
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^(?P<task_id>[0-9]+)/report/$', views.output_result, name='report'),
    url(r'index/(?P<task_id>[0-9]+)/$', views.delete_task, name='delete_task'),
    url(r'delete/(?P<iObject_id>[0-9]+)/$', views.delete_i_object, name='delete_i_object'),
    url(r'^index/$', views.login_to_index, name='login_to_index'),
    url(r'^(?P<task_id>[0-9]+)/$', views.injection_object, name='injection_object'),
    url(r'^\d+/(?P<iObject_id>[0-9]+)/$', views.execute_injection, name='injection_check'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/injection_test/img/favicon.ico'), name='favicon'),
    url(r'^$', views.login1, name='login'),
    url(r'^logout/$', views.logout_from_index, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^quick_scan/$', views.quick_scan, name='quick_scan'),
    url(r'^for_test/$', views.for_test, name='test'),
]