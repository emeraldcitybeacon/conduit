from django_components import Component, register


@register("phone_form")
class PhoneForm(Component):
    """Component to render a single phone form in a formset."""

    template_file = "phone_form.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {"form": kwargs["form"]}
