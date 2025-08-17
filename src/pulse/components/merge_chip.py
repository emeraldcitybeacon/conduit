"""Merge conflict resolution chip component."""
from __future__ import annotations

from django_components import Component, register


@register("merge_chip")
class MergeChip(Component):
    """Render a chip allowing users to accept server values during conflicts."""

    template_file = "merge_chip.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {
            "path": kwargs.get("path", ""),
            "current": kwargs.get("current", ""),
            "label": kwargs.get("label", "Use latest"),
        }
