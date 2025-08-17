"""Right-hand shelf drawer listing queued resources."""
from __future__ import annotations

from django_components import Component, register

from hsds_ext.models import Shelf


@register("shelf_drawer")
class ShelfDrawer(Component):
    """Render the shelf drawer for the current user."""

    template_file = "shelf_drawer.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - data fetch
        """Assemble template context for the drawer component.

        Args:
            args: Positional component arguments (unused).
            kwargs: Keyword component arguments (unused).
            slots: Named template slots (unused).
            context: Rendering context expected to contain the request.

        Returns:
            dict: Mapping with ``shelf`` and ``members`` for template rendering.
        """

        request = context.get("request")
        shelf = (
            Shelf.objects.filter(owner=request.user)
            .order_by("created_at")
            .first()
            if request and request.user.is_authenticated
            else None
        )
        members: list[dict[str, object]] = []
        if shelf:
            members = [
                {"entity_type": m.entity_type, "entity_id": m.entity_id}
                for m in shelf.members.order_by("-added_at")
            ]
        return {"shelf": shelf, "members": members}
