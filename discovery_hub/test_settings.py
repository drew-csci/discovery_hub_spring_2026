import os
from .settings import *

# Override database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use in-memory database for faster testing
SECRET_KEY = 'test-secret-key-for-testing-only'

# Disable password validators for testing
AUTH_PASSWORD_VALIDATORS = []

# Use test media root
MEDIA_ROOT = BASE_DIR / 'test_media'