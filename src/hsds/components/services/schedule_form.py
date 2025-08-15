from django_components import Component, register


@register("schedule_form")
class ScheduleForm(Component):
    """Component to render a single schedule form in a formset."""

    template_file = "schedule_form.html"

    class View:  # pragma: no cover - simple configuration
        public = True

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        return {"form": kwargs["form"]}
