"""Endpoints and helpers providing sibling service information."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service


@dataclass
class SimpleService:
    """Lightweight representation of a service for sibling lists."""

    id: str
    name: str


def build_sibling_context(service: Service) -> Dict[str, Any]:
    """Return sibling services and navigation metadata for a service."""

    org_qs = (
        Service.objects.filter(organization=service.organization)
        .exclude(id=service.id)
        .order_by("name")
    )
    org_siblings = [SimpleService(str(s.id), s.name) for s in org_qs]

    location = service.locations.first()
    loc_siblings: List[SimpleService] = []
    prev_id = next_id = ""
    first_loc = ""
    if location:
        loc_all = list(location.services.order_by("name"))
        loc_siblings = [
            SimpleService(str(s.id), s.name) for s in loc_all if s.id != service.id
        ]
        ids = [str(s.id) for s in loc_all]
        try:
            idx = ids.index(str(service.id))
            if idx > 0:
                prev_id = ids[idx - 1]
            if idx + 1 < len(ids):
                next_id = ids[idx + 1]
        except ValueError:  # pragma: no cover - defensive
            pass
        if loc_siblings:
            first_loc = loc_siblings[0].id

    first_org = org_siblings[0].id if org_siblings else ""

    return {
        "loc_siblings": loc_siblings,
        "org_siblings": org_siblings,
        "prev_id": prev_id,
        "next_id": next_id,
        "first_loc": first_loc,
        "first_org": first_org,
    }


class SiblingServiceView(APIView):
    """Return services related by organization or location."""

    def get(self, request, id: str) -> Response:
        service = get_object_or_404(
            Service.objects.select_related("organization").prefetch_related("locations"),
            id=id,
        )

        context = build_sibling_context(service)
        return Response(
            {
                "organization": [asdict(s) for s in context["org_siblings"]],
                "location": [asdict(s) for s in context["loc_siblings"]],
            }
        )
