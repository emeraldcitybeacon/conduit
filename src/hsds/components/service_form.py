from django_components import Component, register


@register("service_form")
class ServiceForm(Component):
    """Component to render the service form with nested phone and schedule formsets."""

    template_file = "service_form.html"

    class View:  # pragma: no cover - simple configuration
        public = True

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        form = kwargs["form"]
        return {
            "form": form,
            "phone_formset": kwargs["phone_formset"],
            "schedule_formset": kwargs["schedule_formset"],
            "action": kwargs.get("action", ""),
            "model_name": form._meta.model._meta.verbose_name,
        }
