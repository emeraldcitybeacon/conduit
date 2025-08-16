"""Field freshness badge component."""
from __future__ import annotations

from django_components import register

from ..ui import PulseComponent


@register("freshness_badge")
class FreshnessBadge(PulseComponent):
    """Render a small badge indicating field verification freshness.

    Parameters accepted via component kwargs:
        status: Text label for freshness (e.g., "verified", "stale").
    """

    template_file = "freshness_badge.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {"status": kwargs.get("status", "unknown")}
