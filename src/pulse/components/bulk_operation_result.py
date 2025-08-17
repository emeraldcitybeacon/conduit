"""Component displaying the result of a committed bulk operation."""
from __future__ import annotations

from django_components import Component, register


@register("bulk_operation_result")
class BulkOperationResult(Component):
    """Render the commit result for a bulk operation."""

    template_file = "bulk_operation_result.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        """Expose the bulk operation to the template."""

        return {"operation": kwargs.get("operation")}

