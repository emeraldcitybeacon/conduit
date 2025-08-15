"""Admin registrations for HSDS extension models."""
from __future__ import annotations

from django.contrib import admin

from .models.verification import VerificationEvent
from .models.versions import FieldVersion
from .models.sensitive import SensitiveOverlay


@admin.register(VerificationEvent)
class VerificationEventAdmin(admin.ModelAdmin):
    """Admin configuration for verification events."""

    list_display = ("entity_type", "entity_id", "field_path", "method", "verified_at", "verified_by")
    list_filter = ("entity_type", "method")
    search_fields = ("field_path", "note")


@admin.register(FieldVersion)
class FieldVersionAdmin(admin.ModelAdmin):
    """Admin configuration for field versions."""

    list_display = ("entity_type", "entity_id", "field_path", "version", "updated_at", "updated_by")
    list_filter = ("entity_type",)
    search_fields = ("field_path",)


@admin.register(SensitiveOverlay)
class SensitiveOverlayAdmin(admin.ModelAdmin):
    """Admin configuration for sensitive overlays."""

    list_display = ("entity_type", "entity_id", "sensitive")
    list_filter = ("entity_type", "sensitive")
    search_fields = ("entity_id",)
