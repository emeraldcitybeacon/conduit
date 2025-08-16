"""Endpoints for approving or rejecting draft resources."""
from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Location, Organization, Service
from hsds_ext.models import DraftResource, FieldVersion, VerificationEvent
from resources.permissions import IsEditor
from resources.utils.json_paths import iter_paths


class DraftApproveView(APIView):
    """Approve a ``DraftResource`` and materialize HSDS records."""

    permission_classes = [IsEditor]

    def post(self, request: Request, id: str) -> Response:
        """Write the draft payload to HSDS and mark it approved."""

        draft = get_object_or_404(
            DraftResource, id=id, status=DraftResource.Status.DRAFT
        )
        payload: dict[str, Any] = draft.payload

        # --- Create canonical HSDS objects ---------------------------------
        org_data = payload.get("organization", {})
        organization = Organization.objects.create(
            name=org_data.get("name", "Unnamed"),
            description=org_data.get("description", ""),
        )

        loc_data = payload.get("location") or {}
        location = None
        if loc_data:
            location = Location.objects.create(
                organization=organization,
                name=loc_data.get("name"),
                location_type=loc_data.get(
                    "location_type", Location.LocationType.PHYSICAL
                ),
            )

        svc_data = payload.get("service", {})
        service = Service.objects.create(
            organization=organization,
            name=svc_data.get("name", "Unnamed"),
            status=svc_data.get("status", Service.Status.ACTIVE),
            url=svc_data.get("url"),
            email=svc_data.get("email"),
        )
        if location:
            service.locations.add(location)

        # --- Log versions and provenance -----------------------------------
        for path in iter_paths(payload):
            root = path.split(".", 1)[0]
            entity_id = None
            entity_type = None
            if root == "organization":
                entity_type = FieldVersion.EntityType.ORGANIZATION
                v_entity = VerificationEvent.EntityType.ORGANIZATION
                entity_id = organization.id
            elif root == "location" and location is not None:
                entity_type = FieldVersion.EntityType.LOCATION
                v_entity = VerificationEvent.EntityType.LOCATION
                entity_id = location.id
            elif root == "service":
                entity_type = FieldVersion.EntityType.SERVICE
                v_entity = VerificationEvent.EntityType.SERVICE
                entity_id = service.id
            else:
                continue

            FieldVersion.objects.update_or_create(
                entity_type=entity_type,
                entity_id=entity_id,
                field_path=path,
                defaults={"updated_by": request.user},
            )
            VerificationEvent.objects.create(
                entity_type=v_entity,
                entity_id=entity_id,
                field_path=path,
                method=VerificationEvent.Method.OTHER,
                note="draft approved",
                verified_by=request.user,
            )

        draft.status = DraftResource.Status.APPROVED
        draft.review_note = request.data.get("note")
        draft.save(update_fields=["status", "review_note"])

        return Response(
            {"status": draft.status, "service_id": str(service.id)},
            status=status.HTTP_200_OK,
        )


class DraftRejectView(APIView):
    """Reject a ``DraftResource`` with an optional note."""

    permission_classes = [IsEditor]

    def post(self, request: Request, id: str) -> Response:
        """Mark the draft as rejected and store the note."""

        draft = get_object_or_404(
            DraftResource, id=id, status=DraftResource.Status.DRAFT
        )
        draft.status = DraftResource.Status.REJECTED
        draft.review_note = request.data.get("note")
        draft.save(update_fields=["status", "review_note"])
        return Response({"status": draft.status}, status=status.HTTP_200_OK)
