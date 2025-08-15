from django_components import Component, register


@register("organization_form")
class OrganizationForm(Component):
    """Component to render the organization form."""

    template_file = "organization_form.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {"form": kwargs["form"], "action": kwargs.get("action", "")}
