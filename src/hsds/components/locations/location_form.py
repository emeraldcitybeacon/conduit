from django_components import Component, register


@register("location_form")
class LocationForm(Component):
    """Component to render the location form with nested address, phone, and schedule formsets."""

    template_file = "location_form.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {
            "form": kwargs["form"],
            "address_formset": kwargs["address_formset"],
            "phone_formset": kwargs["phone_formset"],
            "schedule_formset": kwargs["schedule_formset"],
            "action": kwargs.get("action", ""),
        }
