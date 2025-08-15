"""Optional models for taxonomy extensions."""
from __future__ import annotations

import uuid

from django.db import models


class TaxonomyExtension(models.Model):
    """Store additional taxonomy metadata for HSDS entities."""

    class EntityType(models.TextChoices):
        """HSDS entity types to which taxonomy extensions may apply."""

        ORGANIZATION = "organization", "Organization"
        LOCATION = "location", "Location"
        SERVICE = "service", "Service"
        SERVICE_AT_LOCATION = "service_at_location", "Service at Location"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=32, choices=EntityType.choices)
    entity_id = models.UUIDField()
    namespace = models.TextField()
    key = models.TextField()
    value = models.JSONField()

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_taxonomy_extensions"
        unique_together = ("entity_type", "entity_id", "namespace", "key")

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"{self.entity_type}:{self.namespace}:{self.key}"
