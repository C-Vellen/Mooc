from django.urls import path, re_path
from .import views


app_name = 'tuto'

urlpatterns =[

        re_path(r'^$', views.listing, name='listing'),
        re_path(r'^category/(?P<cat_slug>[a-zA-Z0-9-_]+)/$', views.listing_cat, name='listing_cat'),
        re_path(r'^search/', views.listing_search, name='listing_search'),
        re_path(r'^(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.listing_one, name='listing_one'),
        re_path(r'^creation/tutoriel$', views.create_tuto, name='create_tuto'),
        re_path(r'^(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.read_tuto, name='read_tuto'),
        re_path(r'^(?P<tuto_slug>[a-zA-Z0-9-_]+)/(?P<page>[0-9]*)/$', views.read_tuto, name='read_tuto'),
        re_path(r'^update/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.update_tuto, name='update_tuto'),
        re_path(r'^submit/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.submit_tuto, name='submit_tuto'),
        re_path(r'^reject/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.reject_tuto, name='reject_tuto'),
        re_path(r'^publish/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.publish_tuto, name='publish_tuto'),
        re_path(r'^archive/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.archive_tuto, name='archive_tuto'),
        re_path(r'^dearchive/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.dearchive_tuto, name='dearchive_tuto'),
        re_path(r'^depublish/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.depublish_tuto, name='depublish_tuto'),
        re_path(r'^duplicate/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.duplicate_tuto, name='duplicate_tuto'),
        re_path(r'^delete/(?P<tuto_slug>[a-zA-Z0-9-_]+)$', views.delete_tuto, name='delete_tuto'),
 
        ]



