"""Component for rendering field-level diffs."""
from __future__ import annotations

from django_components import Component, register


@register("diff")
class Diff(Component):
    """Render a table of changes from a JSON Patch."""

    template_file = "diff.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple passthrough
        return {"changes": kwargs.get("changes", [])}
