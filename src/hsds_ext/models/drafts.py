"""Models for storing draft composite HSDS resources."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class DraftResource(models.Model):
    """A draft resource composed of HSDS entities pending review."""

    class Status(models.TextChoices):
        """Review status of the draft."""

        DRAFT = "draft", "Draft"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="draft_resources",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.DRAFT
    )
    payload = models.JSONField(help_text="Composite HSDS payload for review.")
    review_note = models.TextField(blank=True, null=True)

    class Meta:
        """Model metadata."""

        db_table = "hsds_ext_draft_resources"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        """Return string representation for admin."""
        return f"Draft {self.id} ({self.status})"
