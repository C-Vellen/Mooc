from django.urls import path, re_path
from . import views


app_name = 'progress'

urlpatterns = [
    re_path(r'^compte$', views.compte, name='compte'),
    re_path(r'^admin/(?P<role>[a-zA-Z0-9-_]+)$', views.admin, name='admin'),
    ]
