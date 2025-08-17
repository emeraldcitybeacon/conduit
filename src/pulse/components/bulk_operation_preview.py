"""Component rendering a bulk operation preview table."""
from __future__ import annotations

from django_components import Component, register


@register("bulk_operation_preview")
class BulkOperationPreview(Component):
    """Render the preview for a staged bulk operation."""

    template_file = "bulk_operation_preview.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        """Provide the bulk operation to the template."""

        return {"operation": kwargs.get("operation")}

