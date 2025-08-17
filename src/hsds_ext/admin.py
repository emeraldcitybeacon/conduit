"""Admin registrations for HSDS extension models."""
from __future__ import annotations

from django.contrib import admin

from .models.bulk_ops import BulkOperation
from .models.change_requests import ChangeRequest
from .models.drafts import DraftResource
from .models.sensitive import SensitiveOverlay
from .models.shelves import Shelf, ShelfMember
from .models.worklists import Worklist
from .models.taxonomy_ext import TaxonomyExtension
from .models.verification import VerificationEvent
from .models.versions import FieldVersion


@admin.register(VerificationEvent)
class VerificationEventAdmin(admin.ModelAdmin):
    """Admin configuration for verification events."""

    list_display = (
        "entity_type",
        "entity_id",
        "field_path",
        "method",
        "verified_at",
        "verified_by",
    )
    list_filter = ("entity_type", "method")
    search_fields = ("field_path", "note")


@admin.register(FieldVersion)
class FieldVersionAdmin(admin.ModelAdmin):
    """Admin configuration for field versions."""

    list_display = (
        "entity_type",
        "entity_id",
        "field_path",
        "version",
        "updated_at",
        "updated_by",
    )
    list_filter = ("entity_type",)
    search_fields = ("field_path",)


@admin.register(SensitiveOverlay)
class SensitiveOverlayAdmin(admin.ModelAdmin):
    """Admin configuration for sensitive overlays."""

    list_display = ("entity_type", "entity_id", "sensitive")
    list_filter = ("entity_type", "sensitive")
    search_fields = ("entity_id",)


@admin.register(DraftResource)
class DraftResourceAdmin(admin.ModelAdmin):
    """Admin configuration for draft resources."""

    list_display = ("id", "status", "created_by", "created_at")
    list_filter = ("status",)
    search_fields = ("id",)


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    """Admin configuration for change requests."""

    list_display = (
        "id",
        "target_entity_type",
        "target_entity_id",
        "status",
        "submitted_by",
        "submitted_at",
    )
    list_filter = ("status", "target_entity_type")
    search_fields = ("target_entity_id", "note")


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    """Admin configuration for shelves."""

    list_display = ("name", "owner", "is_shared", "created_at")
    list_filter = ("is_shared",)
    search_fields = ("name",)


@admin.register(ShelfMember)
class ShelfMemberAdmin(admin.ModelAdmin):
    """Admin configuration for shelf members."""

    list_display = (
        "shelf",
        "entity_type",
        "entity_id",
        "added_by",
        "added_at",
    )
    list_filter = ("entity_type",)
    search_fields = ("entity_id",)


@admin.register(Worklist)
class WorklistAdmin(admin.ModelAdmin):
    """Admin configuration for worklists."""

    list_display = ("name", "owner", "query", "is_shared", "created_at")
    list_filter = ("is_shared",)
    search_fields = ("name", "query")


@admin.register(BulkOperation)
class BulkOperationAdmin(admin.ModelAdmin):
    """Admin configuration for bulk operations."""

    list_display = (
        "id",
        "scope",
        "status",
        "initiated_by",
        "initiated_at",
    )
    list_filter = ("scope", "status")
    search_fields = ("id",)


@admin.register(TaxonomyExtension)
class TaxonomyExtensionAdmin(admin.ModelAdmin):
    """Admin configuration for taxonomy extensions."""

    list_display = ("entity_type", "entity_id", "namespace", "key")
    list_filter = ("entity_type", "namespace")
    search_fields = ("key",)
