from django.urls import re_path
from . import views

urlpatterns = [
    # Catch-all path to spit anything to lead.
    re_path(r'^$', views.get_user_list, name='get_user_list'),
]
