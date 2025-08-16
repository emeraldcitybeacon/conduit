"""API endpoints for shelf management and membership."""
from __future__ import annotations

import uuid

from django.shortcuts import get_object_or_404
from django_components import component_registry
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds_ext.models import Shelf, ShelfMember
from resources.permissions import IsVolunteer

VALID_ENTITY_TYPES = {"organization", "location", "service"}


class ShelfListCreateView(APIView):
    """List shelves for the current user or create a new shelf."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request: Request) -> Response:
        """Return shelves owned by the requesting user."""

        shelves = (
            Shelf.objects.filter(owner=request.user)
            .order_by("-created_at")
            .values("id", "name", "created_at")
        )
        data = [
            {"id": str(s["id"]), "name": s["name"], "created_at": s["created_at"]}
            for s in shelves
        ]
        return Response(data)

    def post(self, request: Request) -> Response:
        """Create a new shelf owned by the requesting user."""

        name = request.data.get("name")
        if not name:
            return Response(
                {"detail": "Name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        shelf = Shelf.objects.create(owner=request.user, name=name)
        return Response(
            {"id": str(shelf.id), "name": shelf.name},
            status=status.HTTP_201_CREATED,
        )


class ShelfDetailView(APIView):
    """Retrieve or delete a shelf along with its members."""

    permission_classes = [IsVolunteer]

    def _get_shelf(self, request: Request, id: str) -> Shelf:
        """Return the shelf owned by the user or raise 404."""

        return get_object_or_404(Shelf, id=id, owner=request.user)

    def get(self, request: Request, id: str) -> Response:
        """Return shelf metadata and member list."""

        shelf = self._get_shelf(request, id)
        members = [
            {
                "id": str(m.id),
                "entity_type": m.entity_type,
                "entity_id": str(m.entity_id),
            }
            for m in shelf.members.order_by("-added_at")
        ]
        return Response(
            {"id": str(shelf.id), "name": shelf.name, "members": members}
        )

    def delete(self, request: Request, id: str) -> Response:
        """Delete the shelf owned by the user."""

        shelf = self._get_shelf(request, id)
        shelf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShelfMemberAddView(APIView):
    """Add a member to the shelf and return the rendered row component."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request: Request, id: str) -> Response:
        """Add the specified entity to the shelf.

        Validates the entity type and identifier before creating or returning an
        existing :class:`ShelfMember` entry. The rendered ``shelf_member_row``
        component is returned so HTMX can insert it into the drawer.
        """

        shelf = get_object_or_404(Shelf, id=id, owner=request.user)
        entity_type = request.data.get("entity_type")
        entity_id = request.data.get("entity_id")

        if entity_type not in VALID_ENTITY_TYPES:
            return Response(
                {"detail": "Invalid entity_type."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            entity_uuid = uuid.UUID(str(entity_id))
        except (ValueError, TypeError):  # pragma: no cover - defensive
            return Response(
                {"detail": "Invalid entity_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member, created = ShelfMember.objects.get_or_create(
            shelf=shelf,
            entity_type=entity_type,
            entity_id=entity_uuid,
            defaults={"added_by": request.user},
        )

        component_cls = component_registry.registry.get("shelf_member_row")
        html = component_cls.render(
            kwargs={
                "shelf_id": str(shelf.id),
                "entity_type": member.entity_type,
                "entity_id": str(member.entity_id),
            },
            request=request,
        )
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(html, status=status_code)


class ShelfMemberRemoveView(APIView):
    """Remove a member from the shelf."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request: Request, id: str) -> Response:
        """Remove the specified entity from the shelf.

        If the entity does not exist on the shelf, the operation is silently
        ignored so that ``204`` can still be returned for idempotence.
        """

        shelf = get_object_or_404(Shelf, id=id, owner=request.user)
        entity_type = request.data.get("entity_type")
        entity_id = request.data.get("entity_id")

        if entity_type not in VALID_ENTITY_TYPES:
            return Response(
                {"detail": "Invalid entity_type."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            entity_uuid = uuid.UUID(str(entity_id))
        except (ValueError, TypeError):  # pragma: no cover - defensive
            return Response(
                {"detail": "Invalid entity_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ShelfMember.objects.filter(
            shelf=shelf, entity_type=entity_type, entity_id=entity_uuid
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

