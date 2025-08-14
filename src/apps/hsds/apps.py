"""App configuration for HSDS models."""
from django.apps import AppConfig


class HsdsConfig(AppConfig):
    """Configuration for the HSDS app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.hsds"
    verbose_name = "HSDS Core"
