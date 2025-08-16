"""Generic modal dialog component using daisyUI."""
from __future__ import annotations

from django_components import register

from . import PulseComponent


@register("modal")
class Modal(PulseComponent):
    """Render a modal dialog with optional title and slot content."""

    template_file = "modal.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {
            "id": kwargs.get("id", "modal"),
            "title": kwargs.get("title", ""),
            "content": slots.get("default", ""),
        }
