"""API endpoints for composite Resources."""
from __future__ import annotations

import json
from typing import Any, Dict

from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import BaseParser, FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service
from hsds_ext.models import FieldVersion, SensitiveOverlay
from resources.permissions import IsVolunteer
from resources.serializers.resource import ResourceSerializer
from resources.utils.etags import assert_versions, resource_etag
from resources.utils.json_paths import get_value, iter_paths, set_value


class OctetStreamParser(BaseParser):
    """Parse ``application/octet-stream`` bodies into a ``QueryDict``."""

    media_type = "application/octet-stream"

    def parse(self, stream, media_type=None, parser_context=None):  # pragma: no cover - simple
        raw = stream.read().decode()
        # Django's test client sends dict repr for octet-stream bodies
        if raw.strip().startswith("{"):
            try:
                return json.loads(raw.replace("'", '"'))
            except (json.JSONDecodeError, UnicodeDecodeError):  # pragma: no cover - defensive
                return {}
        return QueryDict(raw)


class ResourceView(APIView):
    """Retrieve and update composite HSDS resources."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser, MultiPartParser, OctetStreamParser]

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

    def _overlay(self, service: Service) -> SensitiveOverlay | None:
        """Return the SensitiveOverlay for ``service`` if it exists."""

        try:
            return SensitiveOverlay.objects.get(
                entity_type=SensitiveOverlay.EntityType.SERVICE,
                entity_id=service.id,
            )
        except SensitiveOverlay.DoesNotExist:
            return None

    def get(self, request: Request, id: str) -> Response:
        """Return the composed resource with ETag header."""

        service = self._get_service(id)
        versions = self._version_map(service)
        overlay = self._overlay(service)
        serializer = ResourceSerializer(
            {
                "service": service,
                "organization": service.organization,
                "location": next(iter(service.locations.all()), None),
            },
            context={"versions": versions, "sensitive_overlay": overlay},
        )
        etag = resource_etag(versions)
        return Response(serializer.data, headers={"ETag": etag})

    def patch(self, request: Request, id: str) -> Response:
        """Apply partial updates to auto-publish fields with optimistic locking."""

        service = self._get_service(id)
        versions = self._version_map(service)
        current_etag = resource_etag(versions)
        if request.headers.get("If-Match") != current_etag:
            overlay = self._overlay(service)
            data = ResourceSerializer(
                {
                    "service": service,
                    "organization": service.organization,
                    "location": next(iter(service.locations.all()), None),
                },
                context={"versions": versions, "sensitive_overlay": overlay},
            ).data
            fields = []
            if isinstance(request.data, QueryDict):
                for key in request.data.keys():
                    if key in {"assert_versions", "csrfmiddlewaretoken"}:
                        continue
                    fields.append(key)
            else:
                for path in iter_paths(request.data):
                    if not path.startswith("assert_versions"):
                        fields.append(path)
            current = {path: get_value(data, path) for path in fields}
            return Response(
                {"detail": "Precondition Failed", "etags": data["etags"], "current": current},
                status=status.HTTP_412_PRECONDITION_FAILED,
            )

        mismatches = assert_versions(versions, request.data.get("assert_versions", {}))
        if mismatches:
            overlay = self._overlay(service)
            data = ResourceSerializer(
                {
                    "service": service,
                    "organization": service.organization,
                    "location": next(iter(service.locations.all()), None),
                },
                context={"versions": versions, "sensitive_overlay": overlay},
            ).data
            current = {path: get_value(data, path) for path in mismatches}
            return Response(
                {
                    "detail": "Version mismatch",
                    "mismatches": mismatches,
                    "etags": data["etags"],
                    "current": current,
                },
                status=status.HTTP_409_CONFLICT,
            )

        incoming: Dict[str, Any]
        if isinstance(request.data, (QueryDict, dict)):
            # Convert dotted keys like ``service.url`` into nested structures.
            incoming = {}
            items = request.data.items() if isinstance(request.data, QueryDict) else request.data.items()
            for key, value in items:
                set_value(incoming, key, value)
        else:
            incoming = request.data

        overlay = self._overlay(service)
        serializer = ResourceSerializer(
            {
                "service": service,
                "organization": service.organization,
                "location": next(iter(service.locations.all()), None),
            },
            data=incoming,
            partial=True,
            context={
                "versions": versions,
                "user": request.user,
                "sensitive_overlay": overlay,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        versions = self._version_map(service)
        overlay = self._overlay(service)
        data = ResourceSerializer(
            {
                "service": service,
                "organization": service.organization,
                "location": next(iter(service.locations.all()), None),
            },
            context={"versions": versions, "sensitive_overlay": overlay},
        ).data
        new_etag = resource_etag(versions)
        return Response(data, headers={"ETag": new_etag})
