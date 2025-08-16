from django_components import Component, register


@register("organization_form")
class OrganizationForm(Component):
    """Component to render the organization form."""

    template_file = "organization_form.html"

    class View:  # pragma: no cover - simple configuration
        public = True

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        form = kwargs["form"]
        return {
            "form": form,
            "action": kwargs.get("action", ""),
            "model_name": form._meta.model._meta.verbose_name,
        }
