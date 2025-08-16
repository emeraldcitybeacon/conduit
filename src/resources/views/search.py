"""Search endpoint for duplicate detection."""
from __future__ import annotations

from typing import Any, Dict, List

from django.db.models import Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Location, Organization, Phone, Service
from resources.permissions import IsVolunteer


class SearchView(APIView):
    """Simple fuzzy search across core HSDS entities.

    This endpoint is used for live duplicate hints. It performs a very basic
    `icontains` search across organization, service, location names as well as
    phone numbers and address lines. Results are intentionally lightweight and
    limited in number to keep the response fast.
    """

    permission_classes = [IsVolunteer]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Return a list of candidate matches for the provided query string."""

        query = request.query_params.get("q", "").strip()
        if not query:
            return Response(
                {"detail": "q parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results: List[Dict[str, Any]] = []

        # Organization name search
        for org in Organization.objects.filter(name__icontains=query)[:5]:
            results.append(
                {
                    "type": "organization",
                    "id": str(org.id),
                    "name": org.name,
                }
            )

        # Service name search
        for svc in Service.objects.filter(name__icontains=query)[:5]:
            results.append(
                {
                    "type": "service",
                    "id": str(svc.id),
                    "name": svc.name,
                }
            )

        # Location name or address search
        locations = (
            Location.objects.filter(
                Q(name__icontains=query)
                | Q(addresses__address_1__icontains=query)
                | Q(addresses__city__icontains=query)
            )
            .prefetch_related("addresses")
            .distinct()[:5]
        )
        for loc in locations:
            addr_obj = loc.addresses.first()
            addr = (
                f"{addr_obj.address_1}, {addr_obj.city}" if addr_obj else ""
            )
            results.append(
                {
                    "type": "location",
                    "id": str(loc.id),
                    "name": loc.name or addr,
                    "address": addr,
                }
            )

        # Phone number search (maps back to owning entity)
        phones = Phone.objects.filter(number__icontains=query).select_related(
            "service", "organization", "location"
        )[:5]
        for ph in phones:
            entity = ph.service or ph.location or ph.organization
            if not entity:
                continue
            results.append(
                {
                    "type": entity.__class__.__name__.lower(),
                    "id": str(entity.id),
                    "name": getattr(entity, "name", ""),
                    "phone": ph.number,
                }
            )

        return Response({"results": results})
