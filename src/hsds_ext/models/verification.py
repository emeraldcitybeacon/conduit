"""Models for recording verification events of HSDS fields."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class VerificationEvent(models.Model):
    """A record of a field verification for an HSDS entity."""

    class EntityType(models.TextChoices):
        """Types of HSDS entities subject to verification."""

        ORGANIZATION = "organization", "Organization"
        LOCATION = "location", "Location"
        SERVICE = "service", "Service"
        SERVICE_AT_LOCATION = "service_at_location", "Service at Location"

    class Method(models.TextChoices):
        """Methods by which a field can be verified."""

        CALLED = "called", "Called"
        WEBSITE = "website", "Website"
        ONSITE = "onsite", "On-site"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=32, choices=EntityType.choices)
    entity_id = models.UUIDField()
    field_path = models.TextField(help_text="Dot-path of the verified field within HSDS JSON.")
    method = models.CharField(max_length=16, choices=Method.choices)
    note = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_events",
    )

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_verification_events"
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["-verified_at"]),
            models.Index(fields=["field_path"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"{self.entity_type}:{self.field_path} by {self.verified_by}"
