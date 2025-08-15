"""Component for rendering organization forms."""
from __future__ import annotations

from django_components import Component, register


@register("organization-form")
class OrganizationForm(Component):
    """Render the organization form with HTMX attributes."""

    template_file = "hsds/includes/organization_form.html"

    def get_template_data(self, *args, **kwargs):
        """Expose the bound form to the template."""
        return {"form": kwargs["form"]}
