"""Views for worklist pages."""
from __future__ import annotations

from django.views.generic import TemplateView

from hsds_ext.models import Worklist


class WorklistIndexView(TemplateView):
    """Render a list of the user's worklists."""

    template_name = "pulse/worklists/index.html"

    def get_context_data(self, **kwargs):  # pragma: no cover - simple
        ctx = super().get_context_data(**kwargs)
        ctx["worklists"] = Worklist.objects.filter(owner=self.request.user).order_by(
            "-created_at"
        )
        return ctx
