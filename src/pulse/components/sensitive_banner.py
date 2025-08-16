"""Component rendering a banner for sensitive resources."""
from __future__ import annotations

from django_components import Component, register


@register("sensitive_banner")
class SensitiveBanner(Component):
    """Display a warning banner when a resource is sensitive."""

    template_file = "sensitive_banner.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {"is_sensitive": kwargs.get("is_sensitive", False)}
