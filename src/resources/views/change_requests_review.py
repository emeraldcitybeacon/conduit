"""Approve or reject change requests and apply patches."""
from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service
from hsds_ext.models import ChangeRequest, FieldVersion, VerificationEvent
from resources.permissions import IsEditor
from resources.serializers.resource import ServiceSerializer
from resources.utils.json_patch import apply_patch


class ChangeRequestApproveView(APIView):
    """Apply a pending ``ChangeRequest`` to the target resource."""

    permission_classes = [IsEditor]

    def post(self, request: Request, id: str, *args: Any, **kwargs: Any) -> Response:
        """Apply stored patch and mark the request approved."""

        change_request = get_object_or_404(
            ChangeRequest, id=id, status=ChangeRequest.Status.PENDING
        )
        service = get_object_or_404(Service, id=change_request.target_entity_id)

        original = {"service": ServiceSerializer(service).data}
        patched = apply_patch(original, change_request.patch)
        service_data = patched.get("service", {})

        changed_fields: list[str] = []
        for field, value in service_data.items():
            if field == "id":
                continue
            if getattr(service, field) != value:
                setattr(service, field, value)
                changed_fields.append(field)
        if changed_fields:
            service.save(update_fields=changed_fields)
            for field in changed_fields:
                path = f"service.{field}"
                FieldVersion.objects.update_or_create(
                    entity_type=FieldVersion.EntityType.SERVICE,
                    entity_id=service.id,
                    field_path=path,
                    defaults={"updated_by": request.user},
                )
                VerificationEvent.objects.create(
                    entity_type=VerificationEvent.EntityType.SERVICE,
                    entity_id=service.id,
                    field_path=path,
                    method=VerificationEvent.Method.OTHER,
                    note="change request approved",
                    verified_by=request.user,
                )

        change_request.status = ChangeRequest.Status.APPROVED
        change_request.reviewed_by = request.user
        change_request.reviewed_at = timezone.now()
        change_request.save(update_fields=["status", "reviewed_by", "reviewed_at"])

        return Response({"status": change_request.status}, status=status.HTTP_200_OK)


class ChangeRequestRejectView(APIView):
    """Reject a pending ``ChangeRequest``."""

    permission_classes = [IsEditor]

    def post(self, request: Request, id: str, *args: Any, **kwargs: Any) -> Response:
        """Mark the request rejected without applying its patch."""

        change_request = get_object_or_404(
            ChangeRequest, id=id, status=ChangeRequest.Status.PENDING
        )
        change_request.status = ChangeRequest.Status.REJECTED
        change_request.reviewed_by = request.user
        change_request.reviewed_at = timezone.now()
        change_request.save(update_fields=["status", "reviewed_by", "reviewed_at"])
        return Response({"status": change_request.status}, status=status.HTTP_200_OK)
