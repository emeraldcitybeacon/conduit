"""Endpoints for recording verification events on resources."""
from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds_ext.models import VerificationEvent
from resources.permissions import IsVolunteer


class VerifyFieldView(APIView):
    """Create a :class:`VerificationEvent` for a resource field.

    The view expects a POST body containing:
        ``field_path``: Dot path for the field being verified.
        ``method``: Verification method string.
        ``note`` (optional): Free-form note.

    The ``entity_type`` is derived from the prefix of ``field_path``
    (e.g. ``"service.url"`` -> ``VerificationEvent.EntityType.SERVICE``).
    """

    permission_classes = [IsVolunteer]

    def post(self, request: Request, id: str, *args: Any, **kwargs: Any) -> Response:
        """Persist the verification event and return its timestamp."""

        field_path = request.data.get("field_path")
        method = request.data.get("method")
        note = request.data.get("note", "")
        if not field_path or not method:
            return Response(
                {"detail": "field_path and method are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prefix = field_path.split(".", 1)[0]
        try:
            entity_type = VerificationEvent.EntityType(prefix)
        except ValueError:
            return Response(
                {"detail": f"Unknown entity type prefix: {prefix}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event = VerificationEvent.objects.create(
            entity_type=entity_type,
            entity_id=id,
            field_path=field_path,
            method=method,
            note=note or None,
            verified_by=request.user,
        )
        return Response(
            {"verified_at": event.verified_at.isoformat()},
            status=status.HTTP_201_CREATED,
        )
