"""API endpoints for draft resources."""
from __future__ import annotations

from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds_ext.models import DraftResource
from resources.permissions import IsVolunteer


class DraftCreateView(APIView):
    """Create a new ``DraftResource`` from posted composite payload."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser]

    def post(self, request: Request) -> Response:
        """Persist the incoming JSON payload as a ``DraftResource``."""

        draft = DraftResource.objects.create(
            created_by=request.user,
            payload=request.data,
        )
        return Response(
            {"id": str(draft.id), "status": draft.status},
            status=status.HTTP_201_CREATED,
        )


class DraftListView(APIView):
    """List draft resources for the current user."""

    permission_classes = [IsVolunteer]

    def get(self, request: Request) -> Response:
        """Return basic metadata for the user's drafts."""

        drafts = (
            DraftResource.objects.filter(created_by=request.user)
            .order_by("-created_at")
            .values("id", "status", "created_at")
        )
        # Convert UUIDs to strings for JSON serialization
        data = [
            {"id": str(d["id"]), "status": d["status"], "created_at": d["created_at"]}
            for d in drafts
        ]
        return Response(data)
