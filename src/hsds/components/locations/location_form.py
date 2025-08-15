from django_components import Component, register


@register("location_form")
class LocationForm(Component):
    """Component to render the location form with nested address, phone, and schedule formsets."""

    template_file = "location_form.html"

    class View:  # pragma: no cover - simple configuration
        public = True

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        form = kwargs["form"]
        return {
            "form": form,
            "address_formset": kwargs["address_formset"],
            "phone_formset": kwargs["phone_formset"],
            "schedule_formset": kwargs["schedule_formset"],
            "action": kwargs.get("action", ""),
            "model_name": form._meta.model._meta.verbose_name,
        }
