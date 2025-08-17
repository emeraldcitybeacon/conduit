"""DaisyUI stat tile component for health metrics."""
from __future__ import annotations

from django_components import Component, register


@register("health_stat_tile")
class HealthStatTile(Component):
    """Render a clickable stat tile.

    Parameters accepted via kwargs:
        label: Display name of the metric.
        count: Numeric value to show.
        href: URL to link to.
    """

    template_file = "health/stat_tile.html"

    def get_template_data(self, context, *args, **kwargs):  # pragma: no cover - simple
        return {
            "label": kwargs.get("label", ""),
            "count": kwargs.get("count", 0),
            "href": kwargs.get("href", "#"),
        }
