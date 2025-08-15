from django_components import Component, register


@register("form_title")
class FormTitle(Component):
    """Component to render a standardized form title."""

    template_file = "form_title.html"

    class View:  # pragma: no cover - simple configuration
        public = True

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        form = kwargs["form"]
        return {
            "form": form,
            "model_name": kwargs.get("model_name", form._meta.model._meta.verbose_name),
            "tag": kwargs.get("tag", "h2"),
            "classes": kwargs.get("classes", "text-xl font-bold"),
        }
