"""Views for serving registered django-components over HTTP."""
from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django_components import component_registry


def component(request: HttpRequest, name: str) -> HttpResponse:
    """Render a component by its registry name.

    Query parameters are forwarded to the component as keyword arguments. If the
    requested component is not registered, a 404 is raised.
    """

    try:
        component_cls = component_registry.registry.get(name)
    except component_registry.NotRegistered as exc:  # pragma: no cover - simple
        raise Http404(f"Component '{name}' not found") from exc

    kwargs = request.GET.dict()
    return component_cls.render_to_response(request=request, kwargs=kwargs)
