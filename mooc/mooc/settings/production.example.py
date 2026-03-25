import os
from pathlib import Path
from .base import BASE_DIR


SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DEBUG=False
ALLOWED_HOSTS =  ['mondomaine.fr', 'www.mondomaine.fr']
CSRF_TRUSTED_ORIGINS = ["https://mondomaine.fr", "https://www.mondomaine.fr"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql / django.db.backends.postgresql",
        "NAME": "xxxxxx",
        "USER": "xxxxxx",
        "PASSWORD": "xxxxxx",
        "HOST": "xxxxxx",
        "PORT": "xxxx",
    }
}

STATIC_ROOT = "/app/staticfiles"
MEDIA_ROOT = "/app/media"
