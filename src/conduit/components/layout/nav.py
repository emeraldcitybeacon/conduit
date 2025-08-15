from django_components import Component, register


@register("nav")
class Nav(Component):
    template_file = "nav.html"

    class View:  # pragma: no cover - simple configuration
        public = True
