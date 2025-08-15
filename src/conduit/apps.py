"""AppConfig for project-level utilities such as component autodiscovery."""
from __future__ import annotations

from django.apps import AppConfig
from django_components import autodiscover


class ConduitConfig(AppConfig):
    """Configure django-components to discover project components."""

    name = "src.conduit"

    def ready(self) -> None:  # pragma: no cover - import side effects
        """Autodiscover components in installed apps."""
        autodiscover()
