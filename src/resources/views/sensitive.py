"""Endpoints for managing sensitive overlays on resources."""
from __future__ import annotations

from typing import Any, Dict

from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service
from hsds_ext.models import FieldVersion, SensitiveOverlay
from resources.permissions import IsEditor
from resources.serializers.resource import ResourceSerializer
from resources.utils.etags import resource_etag


class ResourceSensitiveView(APIView):
    """Toggle the ``SensitiveOverlay`` for a Service resource."""

    permission_classes = [IsEditor]

    def patch(self, request: Request, id: str) -> Response:
        """Create or update the overlay then return redacted resource data."""

        service = get_object_or_404(
            Service.objects.select_related("organization").prefetch_related("locations"),
            id=id,
        )

        overlay, _ = SensitiveOverlay.objects.get_or_create(
            entity_type=SensitiveOverlay.EntityType.SERVICE,
            entity_id=service.id,
        )

        payload: Dict[str, Any] = request.data or {}
        if "sensitive" in payload:
            overlay.sensitive = bool(payload["sensitive"])
        if "visibility_rules" in payload:
            overlay.visibility_rules = payload.get("visibility_rules") or {}
        overlay.save()

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
            context={"versions": versions, "sensitive_overlay": overlay},
        )
        etag = resource_etag(versions)
        return Response(serializer.data, headers={"ETag": etag})

