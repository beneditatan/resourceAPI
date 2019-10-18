from django.urls import re_path
from . import views

urlpatterns = [
    # Catch-all path to spit anything to lead.
    re_path(r'^$', views.get_user_list, name='get_user_list'),
    re_path(r'^details/(?P<username>[\w-]+)/$', views.user_detail, name='user_detail'),
    re_path(r'^register/$', views.create_user, name='create_user'),
]
