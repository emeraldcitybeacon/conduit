"""Placeholder diff viewer component."""
from __future__ import annotations

from django_components import register

from . import PulseComponent


@register("diff")
class Diff(PulseComponent):
    """Render a very simple two-column diff placeholder."""

    template_file = "diff.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {
            "left": kwargs.get("left", ""),
            "right": kwargs.get("right", ""),
        }
