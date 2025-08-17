"""Single shelf member row with remove control."""
from __future__ import annotations

from django_components import Component, register


@register("shelf_member_row")
class ShelfMemberRow(Component):
    """Render a shelf member entry with a remove button."""

    template_file = "member_row.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        """Provide template variables for a single shelf member row.

        Args:
            args: Positional component arguments (unused).
            kwargs: Keyword arguments expected to contain ``shelf_id``,
                ``entity_type`` and ``entity_id``.
            slots: Template slots (unused).
            context: Rendering context (unused).

        Returns:
            dict: Values inserted into ``shelf_member.html``.
        """

        return {
            "shelf_id": kwargs.get("shelf_id"),
            "entity_type": kwargs.get("entity_type"),
            "entity_id": kwargs.get("entity_id"),
        }
