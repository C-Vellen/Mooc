from django.urls import path, re_path
from . import views


app_name = 'progress'

urlpatterns = [
    re_path(r'^compte$', views.compte, name='compte'),
    re_path(r'^auteur$', views.auteur, name='auteur'),
    re_path(r'^gestionnaire$', views.gestionnaire, name='gestionnaire'),
    ]
