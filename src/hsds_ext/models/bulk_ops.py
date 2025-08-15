"""Models for staging and committing bulk operations."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class BulkOperation(models.Model):
    """Represents a bulk patch staged for multiple HSDS entities."""

    class Scope(models.TextChoices):
        """Scope of the bulk operation."""

        SHELF = "shelf", "Shelf"
        SIBLINGS = "siblings", "Siblings"

    class Status(models.TextChoices):
        """Lifecycle status of the operation."""

        STAGED = "staged", "Staged"
        COMMITTED = "committed", "Committed"
        UNDONE = "undone", "Undone"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bulk_operations",
    )
    initiated_at = models.DateTimeField(auto_now_add=True)
    scope = models.CharField(max_length=16, choices=Scope.choices)
    targets = models.JSONField(help_text="Target entities for the operation.")
    patch = models.JSONField(help_text="RFC6902 patch to apply to targets.")
    preview = models.JSONField(blank=True, null=True, help_text="Precomputed preview data.")
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.STAGED
    )
    undo_token = models.TextField(blank=True, null=True)
    committed_at = models.DateTimeField(blank=True, null=True)
    undone_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_bulk_operations"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"BulkOp {self.id} ({self.status})"
