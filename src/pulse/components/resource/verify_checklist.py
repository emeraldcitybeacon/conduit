"""Verification checklist component."""
from __future__ import annotations

from django_components import Component, register


@register("verify_checklist")
class VerifyChecklist(Component):
    """Render a checklist for verifying common resource details.

    Parameters via component kwargs:
        resource_id: UUID of the service/resource being verified.
    """

    template_file = "resource/verify_checklist.html"

    def get_template_data(self, context, *args, **kwargs):  # pragma: no cover - simple
        return {"resource_id": kwargs.get("resource_id")}
