"""App configuration for HSDS extension models."""
from django.apps import AppConfig


class HsdsExtConfig(AppConfig):
    """Configuration for the hsds_ext app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "hsds_ext"
    verbose_name = "HSDS Extensions"
