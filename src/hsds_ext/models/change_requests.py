"""Models for storing review-required change requests."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class ChangeRequest(models.Model):
    """A user-submitted change requiring editorial review."""

    class EntityType(models.TextChoices):
        """HSDS entity types targeted by the change."""

        ORGANIZATION = "organization", "Organization"
        LOCATION = "location", "Location"
        SERVICE = "service", "Service"
        SERVICE_AT_LOCATION = "service_at_location", "Service at Location"

    class Status(models.TextChoices):
        """Status of the change request."""

        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_entity_type = models.CharField(max_length=32, choices=EntityType.choices)
    target_entity_id = models.UUIDField()
    patch = models.JSONField(help_text="RFC6902 patch against canonical HSDS JSON.")
    note = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="change_requests_submitted",
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="change_requests_reviewed",
        blank=True,
        null=True,
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_change_requests"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["target_entity_type", "target_entity_id"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"CR {self.id} ({self.status})"
