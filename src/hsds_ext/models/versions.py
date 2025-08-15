"""Models for tracking per-field HSDS versions."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class FieldVersion(models.Model):
    """Track the last version of an HSDS field for optimistic locking."""

    class EntityType(models.TextChoices):
        """Enumerate HSDS entity types."""

        ORGANIZATION = "organization", "Organization"
        LOCATION = "location", "Location"
        SERVICE = "service", "Service"
        SERVICE_AT_LOCATION = "service_at_location", "Service at Location"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=32, choices=EntityType.choices)
    entity_id = models.UUIDField()
    field_path = models.TextField()
    version = models.BigIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="field_versions",
    )

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_field_versions"
        unique_together = ("entity_type", "entity_id", "field_path")
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"{self.entity_type}:{self.field_path} v{self.version}"
