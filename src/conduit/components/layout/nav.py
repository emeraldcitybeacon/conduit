from django_components import Component, register


@register("nav")
class Nav(Component):
    template_file = "nav.html"
