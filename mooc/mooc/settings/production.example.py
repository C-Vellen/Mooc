import os
from .base import BASE_DIR


SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DEBUG=False
ALLOWED_HOSTS =  ['mondomaine.fr', 'www.mondomaine.fr']
CSRF_TRUSTED_ORIGINS = ["https://mondomaine.fr", "https://www.mondomaine.fr"]

STATIC_ROOT = "/app/mooc/staticfiles"
MEDIA_ROOT = "/app/mooc/media"
 