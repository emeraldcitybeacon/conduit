"""Views for the Pulse data health dashboard."""
from __future__ import annotations

from urllib.parse import quote

from django.urls import reverse
from django.views.generic import TemplateView

from resources.views.health import get_health_stats


class HealthIndexView(TemplateView):
    """Render the data health dashboard with stat tiles."""

    template_name = "pulse/health/index.html"

    def get_context_data(self, **kwargs):  # pragma: no cover - simple
        ctx = super().get_context_data(**kwargs)
        stats = get_health_stats()
        worklist_base = reverse("pulse:worklists-index")
        ctx["stats"] = [
            {
                "label": "No phone",
                "count": stats["no_phone"],
                "href": f"{worklist_base}?q={quote('no phone')}",
            },
            {
                "label": "No hours",
                "count": stats["no_hours"],
                "href": f"{worklist_base}?q={quote('no hours')}",
            },
            {
                "label": "Not geocoded",
                "count": stats["not_geocoded"],
                "href": f"{worklist_base}?q={quote('not geocoded')}",
            },
            {
                "label": "Stale fields",
                "count": stats["stale"],
                "href": f"{worklist_base}?q={quote('stale fields')}",
            },
        ]
        return ctx
