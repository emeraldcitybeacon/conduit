"""Component rendering a single change request row."""
from __future__ import annotations

from django_components import Component, register


@register("review_request_row")
class ReviewRequestRow(Component):
    """Render a table row for a ``ChangeRequest`` in the review queue."""

    template_file = "review_request_row.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {"change_request": kwargs.get("change_request")}

