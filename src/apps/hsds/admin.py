"""Admin registrations for HSDS core models."""
from django.contrib import admin

from .models import Organization, Program, Service, Location

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin interface for organizations."""

    list_display = ("name", "email", "website")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Admin interface for programs."""

    list_display = ("name", "organization")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for services."""

    list_display = ("name", "organization", "status")
    list_filter = ("status",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin interface for locations."""

    list_display = ("name", "location_type", "organization")
    list_filter = ("location_type",)
