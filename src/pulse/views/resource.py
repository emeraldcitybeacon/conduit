"""Views for the Pulse Resource detail page and section partials."""
from __future__ import annotations

from typing import Any, Dict

from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views import View

from hsds.models import Service
from hsds_ext.models import FieldVersion, VerificationEvent
from resources.serializers.resource import ResourceSerializer


class ResourceDetailView(View):
    """Render the Resource detail shell with tabs.

    The view assembles the composite HSDS resource using the existing
    ``ResourceSerializer`` and passes it to the template for initial rendering.
    Subsequent tab content is loaded via HTMX requests handled by
    :func:`section`.
    """

    template_name = "pulse/resource/detail.html"

    def _serialize(self, service: Service) -> Dict[str, Any]:
        """Return serialized resource data and verification metadata."""

        versions = {
            fv.field_path: fv.version
            for fv in FieldVersion.objects.filter(
                entity_type=FieldVersion.EntityType.SERVICE, entity_id=service.id
            )
        }
        serializer = ResourceSerializer(
            {
                "service": service,
                "organization": service.organization,
                "location": service.locations.first(),
            },
            context={"versions": versions},
        )
        data: Dict[str, Any] = serializer.data

        events = VerificationEvent.objects.filter(
            entity_type=VerificationEvent.EntityType.SERVICE, entity_id=service.id
        ).order_by("-verified_at")

        verifications: Dict[str, Any] = {}
        for ev in events:
            parts = ev.field_path.split(".")
            node = verifications
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node.setdefault(parts[-1], []).append(
                {"method": ev.method, "verified_at": ev.verified_at, "field_path": ev.field_path}
            )

        data["verifications"] = verifications
        return data

    def get(self, request: HttpRequest, id: str) -> HttpResponse:
        service = get_object_or_404(
            Service.objects.select_related("organization").prefetch_related("locations"),
            id=id,
        )
        context = {"resource": self._serialize(service)}
        return render(request, self.template_name, context)


def section(request: HttpRequest, id: str, name: str) -> HttpResponse:
    """Return a stubbed section partial for the resource page."""

    template = f"pulse/resource/{name}_tab.html"
    service = get_object_or_404(Service, id=id)
    detail = ResourceDetailView()
    data = detail._serialize(service)

    context: Dict[str, Any] = {"resource": data}
    if name == "history":
        context["events"] = VerificationEvent.objects.filter(
            entity_type=VerificationEvent.EntityType.SERVICE, entity_id=service.id
        ).order_by("-verified_at")

    try:
        return render(request, template, context)
    except Exception as exc:  # pragma: no cover - template missing
        raise Http404(f"Unknown section: {name}") from exc
