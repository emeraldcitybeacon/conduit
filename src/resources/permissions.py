"""Role-based permission classes and field publish rules."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


AUTO_PUBLISH_FIELDS = {
    "service.url",
    "service.email",
}
"""Paths that volunteers may update directly."""

REVIEW_REQUIRED_FIELDS = {
    "service.name",
    "service.description",
}
"""Paths that require editor review when changed by volunteers."""


class IsVolunteer(BasePermission):
    """Allow any authenticated user to act as a volunteer."""

    def has_permission(self, request, view) -> bool:  # pragma: no cover - simple
        return bool(request.user and request.user.is_authenticated)


class IsEditor(BasePermission):
    """Allow editors and admins."""

    def has_permission(self, request, view) -> bool:  # pragma: no cover - simple
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in {User.Role.EDITOR, User.Role.ADMIN}


class IsAdmin(BasePermission):
    """Allow only admins."""

    def has_permission(self, request, view) -> bool:  # pragma: no cover - simple
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )
