import os
from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE


SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DEBUG=True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]

INSTALLED_APPS += [
    "debug_toolbar",
    "django_browser_reload",
    ]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    ] 

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql / django.db.backends.mysql",
        "NAME": "xxxxxx",
        "USER": "xxxxxx",
        "PASSWORD": "xxxxxx",
        "HOST": "127.0.0.1",
        "PORT": "xxxx",
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

