# Development settings
from .base import *  # noqa: F401,F403
from .base import BASE_DIR

# Enable debug mode for development
DEBUG = True
# CSRF_TRUSTED_ORIGINS = []

# Force disable template caching in development
ENABLE_CACHING = False

# Django Components development settings
COMPONENTS = {
    "autodiscover": True,
}

# Add development-specific apps
INSTALLED_APPS = INSTALLED_APPS + [
    "django_extensions",
]
