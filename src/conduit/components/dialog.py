from django_components import Component, register


@register("dialog")
class Dialog(Component):
    """Component to render dialogs."""

    template_file = "dialog.html"
    js_file = "dialog.js"

    def get_template_data(self, args, kwargs, slots, context):
        return {
            "id": kwargs["id"],
        }
