from django_components import Component, register


@register("schedule_form")
class ScheduleForm(Component):
    """Component to render a single schedule form in a formset."""

    template_file = "schedule_form.html"

    class View:  # pragma: no cover - simple configuration
        public = True

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        form = kwargs["form"]
        return {
            "form": form,
            "model_name": form._meta.model._meta.verbose_name,
        }
