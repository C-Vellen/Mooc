from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^tutoriels/', include('tuto.urls', namespace='tuto')),
    re_path(r'^user/', include('user.urls', namespace='user')),
    re_path(r'^progress/', include('progress.urls', namespace='progress')),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    path("__reload__/", include("django_browser_reload.urls")),

    re_path(r'^', include('home.urls', namespace='home')), # positionner toujours en dernier !

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
            ] + urlpatterns
