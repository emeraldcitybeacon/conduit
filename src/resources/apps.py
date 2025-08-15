"""App configuration for resources facade APIs."""
from django.apps import AppConfig


class ResourcesConfig(AppConfig):
    """Configuration for the resources app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "resources"
    verbose_name = "Resource APIs"
