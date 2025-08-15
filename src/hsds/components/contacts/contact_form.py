from django_components import Component, register


@register("contact_form")
class ContactForm(Component):
    """Component to render the contact form."""

    template_file = "contact_form.html"

    class View:  # pragma: no cover - simple configuration
        public = True

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {"form": kwargs["form"], "action": kwargs.get("action", "")}
