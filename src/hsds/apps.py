"""App configuration for HSDS models."""
from django.apps import AppConfig


class HsdsConfig(AppConfig):
    """Configuration for the HSDS app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "hsds"
    verbose_name = "HSDS Core"

    def ready(self) -> None:  # pragma: no cover - side effects only
        # Import translation definitions so modeltranslation can register
        # translated fields for HSDS models.
        from . import translation  # noqa: F401
