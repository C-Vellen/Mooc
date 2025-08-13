from django.urls import path, re_path
from . import views
from . import apps


app_name = apps.HomeConfig.name

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]


