"""API endpoints for staging and executing bulk operations."""
from __future__ import annotations

import json
import secrets
from typing import Any, List

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds_ext.models import BulkOperation, Shelf
from resources.permissions import IsVolunteer


class BulkOperationStageView(APIView):
    """Create a new :class:`BulkOperation` and return its preview HTML."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request: Request) -> Response:
        """Persist a bulk operation for a shelf and render the preview template."""

        scope = request.data.get("scope")
        if scope != BulkOperation.Scope.SHELF:
            return Response(
                {"detail": "Unsupported scope."}, status=status.HTTP_400_BAD_REQUEST
            )

        shelf_id = request.data.get("shelf_id")
        shelf = get_object_or_404(Shelf, id=shelf_id, owner=request.user)

        patch_raw: Any = request.data.get("patch")
        if isinstance(patch_raw, str):
            try:
                patch: List[dict[str, Any]] = json.loads(patch_raw)
            except json.JSONDecodeError:
                return Response(
                    {"detail": "Invalid patch JSON."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            patch = patch_raw

        if not isinstance(patch, list):
            return Response(
                {"detail": "Patch must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        members = list(shelf.members.all())
        targets = [
            {"entity_type": m.entity_type, "entity_id": str(m.entity_id)} for m in members
        ]
        preview = [
            {
                "entity_type": m.entity_type,
                "entity_id": str(m.entity_id),
                "status": "pending",
            }
            for m in members
        ]

        op = BulkOperation.objects.create(
            initiated_by=request.user,
            scope=BulkOperation.Scope.SHELF,
            targets=targets,
            patch=patch,
            preview=preview,
        )

        html = render_to_string(
            "pulse/shelf/preview.html", {"operation": op}, request=request
        )
        return Response(html, status=status.HTTP_201_CREATED)


class BulkOperationPreviewView(APIView):
    """Return the preview HTML for an existing :class:`BulkOperation`."""

    permission_classes = [IsVolunteer]

    def get(self, request: Request, id: str) -> Response:
        op = get_object_or_404(BulkOperation, id=id, initiated_by=request.user)
        html = render_to_string(
            "pulse/shelf/preview.html", {"operation": op}, request=request
        )
        return Response(html)


class BulkOperationCommitView(APIView):
    """Commit a staged bulk operation and return commit result HTML."""

    permission_classes = [IsVolunteer]

    def post(self, request: Request, id: str) -> Response:
        op = get_object_or_404(BulkOperation, id=id, initiated_by=request.user)
        if op.status != BulkOperation.Status.STAGED:
            return Response(
                {"detail": "Operation not in staged state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        op.status = BulkOperation.Status.COMMITTED
        op.committed_at = timezone.now()
        op.undo_token = secrets.token_urlsafe(16)
        op.save(update_fields=["status", "committed_at", "undo_token"])

        html = render_to_string(
            "pulse/shelf/commit_result.html", {"operation": op}, request=request
        )
        return Response(html)


class BulkOperationUndoView(APIView):
    """Undo a committed bulk operation when provided with a valid token."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request: Request, id: str) -> Response:
        op = get_object_or_404(BulkOperation, id=id, initiated_by=request.user)
        if op.status != BulkOperation.Status.COMMITTED:
            return Response(
                {"detail": "Operation not in committed state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = request.data.get("undo_token")
        if token != op.undo_token:
            return Response(
                {"detail": "Invalid undo token."}, status=status.HTTP_400_BAD_REQUEST
            )

        op.status = BulkOperation.Status.UNDONE
        op.undone_at = timezone.now()
        op.save(update_fields=["status", "undone_at"])
        return Response({"status": op.status})
