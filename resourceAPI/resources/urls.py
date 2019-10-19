from django.urls import re_path
from . import views

urlpatterns = [
    # Catch-all path to spit anything to lead.
    re_path(r'^$', views.create_resource, name='create_resource'),
    re_path(r'^(?P<resource_id>\d+)/$', views.resource_detail, name='resource_detail'),
    re_path(r'^list/(?P<username>[\w-]+)/$', views.get_resources_list, name='get_resources_list'),
    re_path(r'^quota/(?P<username>[\w-]+)/$', views.resource_quota, name='resource_quota'),
]
