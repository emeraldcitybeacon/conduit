"""App configuration for the Pulse frontend."""
from django.apps import AppConfig


class PulseConfig(AppConfig):
    """Configuration for the pulse app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "pulse"
    verbose_name = "Pulse Frontend"
