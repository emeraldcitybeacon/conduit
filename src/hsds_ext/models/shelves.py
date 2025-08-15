"""Models for resource shelves and their members."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class Shelf(models.Model):
    """A user-owned collection of HSDS entities for bulk actions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shelves",
    )
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_shared = models.BooleanField(default=False)

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_shelves"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return self.name


class ShelfMember(models.Model):
    """Link an HSDS entity to a Shelf."""

    class EntityType(models.TextChoices):
        """HSDS entity types that may be stored on a shelf."""

        ORGANIZATION = "organization", "Organization"
        LOCATION = "location", "Location"
        SERVICE = "service", "Service"
        SERVICE_AT_LOCATION = "service_at_location", "Service at Location"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name="members")
    entity_type = models.CharField(max_length=32, choices=EntityType.choices)
    entity_id = models.UUIDField()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shelf_members_added",
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_shelf_members"
        unique_together = ("shelf", "entity_type", "entity_id")

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"{self.entity_type}:{self.entity_id} on {self.shelf_id}"
