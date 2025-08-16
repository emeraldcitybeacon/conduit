"""API endpoints for composite Resources."""
from __future__ import annotations

from typing import Any, Dict

from django.http import QueryDict

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service
from hsds_ext.models import FieldVersion
from resources.permissions import IsVolunteer
from resources.serializers.resource import ResourceSerializer
from resources.utils.etags import assert_versions, resource_etag
from resources.utils.json_paths import set_value


class ResourceView(APIView):
    """Retrieve and update composite HSDS resources."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser]

    def _get_service(self, id: str) -> Service:
        """Return the ``Service`` with its related organization and locations."""

        return get_object_or_404(
            Service.objects.select_related("organization").prefetch_related("locations"),
            id=id,
        )

    def _version_map(self, service: Service) -> Dict[str, int]:
        """Return current field-version map for ``service``."""

        qs = FieldVersion.objects.filter(
            entity_type=FieldVersion.EntityType.SERVICE, entity_id=service.id
        )
        return {fv.field_path: fv.version for fv in qs}

    def get(self, request: Request, id: str) -> Response:
        """Return the composed resource with ETag header."""

        service = self._get_service(id)
        versions = self._version_map(service)
        serializer = ResourceSerializer(
            {"service": service, "organization": service.organization, "location": service.locations.first()},
            context={"versions": versions},
        )
        etag = resource_etag(versions)
        return Response(serializer.data, headers={"ETag": etag})

    def patch(self, request: Request, id: str) -> Response:
        """Apply partial updates to auto-publish fields with optimistic locking."""

        service = self._get_service(id)
        versions = self._version_map(service)
        current_etag = resource_etag(versions)
        if request.headers.get("If-Match") != current_etag:
            return Response({"detail": "Precondition Failed"}, status=status.HTTP_412_PRECONDITION_FAILED)

        mismatches = assert_versions(versions, request.data.get("assert_versions", {}))
        if mismatches:
            return Response(
                {"detail": "Version mismatch", "mismatches": mismatches},
                status=status.HTTP_409_CONFLICT,
            )

        incoming: Dict[str, Any]
        if isinstance(request.data, QueryDict):
            # Convert dotted keys like ``service.url`` into nested structures.
            incoming = {}
            for key, value in request.data.items():
                set_value(incoming, key, value)
        else:
            incoming = request.data

        serializer = ResourceSerializer(
            {"service": service, "organization": service.organization, "location": service.locations.first()},
            data=incoming,
            partial=True,
            context={"versions": versions, "user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        versions = self._version_map(service)
        data = ResourceSerializer(
            {"service": service, "organization": service.organization, "location": service.locations.first()},
            context={"versions": versions},
        ).data
        new_etag = resource_etag(versions)
        return Response(data, headers={"ETag": new_etag})
