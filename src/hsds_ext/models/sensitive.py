"""Models for marking HSDS entities as sensitive and defining visibility rules."""
from __future__ import annotations

import uuid

from django.db import models


class SensitiveOverlay(models.Model):
    """Overlay that marks an HSDS entity as sensitive."""

    class EntityType(models.TextChoices):
        """Enumerate HSDS entity types."""

        ORGANIZATION = "organization", "Organization"
        LOCATION = "location", "Location"
        SERVICE = "service", "Service"
        SERVICE_AT_LOCATION = "service_at_location", "Service at Location"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=32, choices=EntityType.choices)
    entity_id = models.UUIDField()
    sensitive = models.BooleanField(default=False)
    visibility_rules = models.JSONField(default=dict)

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_sensitive_overlays"
        unique_together = ("entity_type", "entity_id")

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"{self.entity_type}:{self.entity_id}"
