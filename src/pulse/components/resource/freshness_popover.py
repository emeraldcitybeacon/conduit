"""Timeline popover showing verification events for a field."""
from __future__ import annotations

from django_components import register

from ..ui import PulseComponent


@register("freshness_popover")
class FreshnessPopover(PulseComponent):
    """Render a popover with a timeline of verification events."""

    template_file = "freshness_popover.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {"events": kwargs.get("events", [])}
