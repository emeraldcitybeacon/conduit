"""Single shelf member row with remove control."""
from __future__ import annotations

from django_components import register

from ..ui import PulseComponent


@register("shelf_member_row")
class ShelfMemberRow(PulseComponent):
    """Render a shelf member entry with a remove button."""

    template_file = "member_row.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {
            "shelf_id": kwargs.get("shelf_id"),
            "entity_type": kwargs.get("entity_type"),
            "entity_id": kwargs.get("entity_id"),
        }

