"""Quick-open command palette component."""
from __future__ import annotations

from django_components import Component, register


@register("worklist_picker")
class WorklistPicker(Component):
    """Render a modal with a search box for quick navigation."""

    template_file = "worklist_picker.html"

    def get_template_data(self, context, *args, **kwargs):  # pragma: no cover - simple
        return {}
