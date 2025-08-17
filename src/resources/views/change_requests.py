"""Endpoints for submitting and listing ChangeRequests."""
from __future__ import annotations

from typing import Any, List

import jsonpatch
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds_ext.models import ChangeRequest
from resources.permissions import IsEditor, IsVolunteer


class ChangeRequestSubmitView(APIView):
    """Create a ``ChangeRequest`` for a service resource."""

    permission_classes = [IsVolunteer]

    def post(self, request: Request, id: str, *args: Any, **kwargs: Any) -> Response:
        """Persist an incoming patch and optional note."""

        patch: List[dict] | None = request.data.get("patch")
        note = request.data.get("note")
        if patch is None:
            return Response(
                {"detail": "patch is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            jsonpatch.JsonPatch(patch)
        except (jsonpatch.JsonPatchException, TypeError):
            return Response(
                {"detail": "invalid patch"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cr = ChangeRequest.objects.create(
            target_entity_type=ChangeRequest.EntityType.SERVICE,
            target_entity_id=id,
            patch=patch,
            note=note or None,
            submitted_by=request.user,
        )
        return Response(
            {"id": str(cr.id), "status": cr.status},
            status=status.HTTP_201_CREATED,
        )


class ChangeRequestQueueView(APIView):
    """List ``ChangeRequest`` objects for reviewer queues."""

    permission_classes = [IsEditor]

    def get(self, request: Request) -> Response:
        """Return change requests filtered by status (default: pending)."""

        status_param = request.query_params.get(
            "status", ChangeRequest.Status.PENDING
        )
        try:
            status_value = ChangeRequest.Status(status_param)
        except ValueError:
            return Response(
                {"detail": f"Invalid status: {status_param}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = (
            ChangeRequest.objects.filter(status=status_value)
            .select_related("submitted_by")
            .order_by("-submitted_at")
        )
        data = [
            {
                "id": str(cr.id),
                "target_entity_type": cr.target_entity_type,
                "target_entity_id": str(cr.target_entity_id),
                "note": cr.note or "",
                "submitted_by": cr.submitted_by.username,
                "submitted_at": cr.submitted_at,
                "patch": cr.patch,
            }
            for cr in qs
        ]
        return Response(data)

