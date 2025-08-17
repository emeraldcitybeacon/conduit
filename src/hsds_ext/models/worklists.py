"""Models for saved search worklists."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class Worklist(models.Model):
    """A saved search query representing a navigable list of resources."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="worklists",
    )
    name = models.TextField()
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_shared = models.BooleanField(default=False)

    class Meta:
        db_table = "hsds_ext_worklists"

    def __str__(self) -> str:  # pragma: no cover - representation
        return self.name
