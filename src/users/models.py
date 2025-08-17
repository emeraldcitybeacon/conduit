"""User model with role-based access control."""
from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model that uses UUID primary key and includes a role field."""

    class Role(models.TextChoices):
        """Enumeration of available user roles."""

        ADMIN = "administrator", "Admin"
        EDITOR = "editor", "Editor"
        VOLUNTEER = "volunteer", "Volunteer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.VOLUNTEER,
        help_text="Designates the user's role within the application.",
    )

    def __str__(self) -> str:  # pragma: no cover - standard representation
        """Return the username as the string representation."""
        return self.username
