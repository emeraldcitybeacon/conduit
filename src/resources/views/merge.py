"""Endpoint for merging duplicate resources."""

from __future__ import annotations

from typing import Any, Dict, List

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service
from hsds_ext.models import FieldVersion
from resources.permissions import IsVolunteer
from resources.serializers.resource import ResourceSerializer
from resources.utils.etags import resource_etag
from resources.utils.json_paths import get_value, set_value


class MergeView(APIView):
    """Apply selected fields from a duplicate to a survivor service."""

    permission_classes = [IsVolunteer]

    def _get_service(self, id: str) -> Service:
        """Return a ``Service`` with organization and locations loaded."""

        return get_object_or_404(
            Service.objects.select_related("organization").prefetch_related("locations"),
            id=id,
        )

    def _version_map(self, service: Service) -> Dict[str, int]:
        """Return a mapping of current ``FieldVersion`` records."""

        qs = FieldVersion.objects.filter(
            entity_type=FieldVersion.EntityType.SERVICE,
            entity_id=service.id,
        )
        return {fv.field_path: fv.version for fv in qs}

    def post(self, request: Request) -> Response:
        """Merge ``duplicate`` into ``survivor`` and delete the duplicate."""

        survivor_id = request.data.get("left_id")
        duplicate_id = request.data.get("right_id")
        fields: List[str] = request.data.get("fields", [])

        if not survivor_id or not duplicate_id:
            return Response(
                {"detail": "left_id and right_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        survivor = self._get_service(survivor_id)
        duplicate = self._get_service(duplicate_id)

        # Build an update payload by pulling selected fields from the duplicate.
        duplicate_doc = ResourceSerializer(
            {
                "service": duplicate,
                "organization": duplicate.organization,
                "location": duplicate.locations.first(),
            },
            context={"versions": {}},
        ).data

        updates: Dict[str, Any] = {}
        for path in fields:
            value = get_value(duplicate_doc, path)
            if value is not None:
                set_value(updates, path, value)

        if not updates:
            return Response(
                {"detail": "no fields selected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        versions = self._version_map(survivor)

        serializer = ResourceSerializer(
            {
                "service": survivor,
                "organization": survivor.organization,
                "location": next(iter(survivor.locations.all()), None),
            },
            data=updates,
            partial=True,
            context={"versions": versions, "user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Remove the duplicate service after successful merge.
        duplicate.delete()

        versions = self._version_map(survivor)
        data = ResourceSerializer(
            {
                "service": survivor,
                "organization": survivor.organization,
                "location": next(iter(survivor.locations.all()), None),
            },
            context={"versions": versions},
        ).data

        return Response(data, headers={"ETag": resource_etag(versions)})

