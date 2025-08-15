"""Role-based permission classes for resource APIs."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsVolunteer(BasePermission):
    """Allow any authenticated user to act as a volunteer."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)


class IsEditor(BasePermission):
    """Allow editors and administrators."""

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in {User.Role.EDITOR, User.Role.ADMINISTRATOR}


class IsAdmin(BasePermission):
    """Allow only administrators."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMINISTRATOR
        )
