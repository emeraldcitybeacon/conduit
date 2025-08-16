from django_components import Component, register


@register("nav")
class Nav(Component):
    template_file = "nav.html"

    def get_template_data(self, args, kwargs, slots, context):
        request = context.get("request")
        user = getattr(request, "user", None)
        return {"user": user}
