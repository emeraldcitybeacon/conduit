"""Admin registrations for HSDS models."""
from django.contrib import admin

from .models import (
    URL,
    Accessibility,
    Address,
    Contact,
    CostOption,
    Funding,
    Language,
    Location,
    Organization,
    OrganizationIdentifier,
    Phone,
    Program,
    RequiredDocument,
    Schedule,
    Service,
    ServiceArea,
    ServiceAtLocation,
    ServiceCapacity,
    Taxonomy,
    TaxonomyTerm,
    Unit,
)


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


admin.site.register(
    [
        Accessibility,
        Address,
        ServiceAtLocation,
        Contact,
        Phone,
        Schedule,
        CostOption,
        Funding,
        Language,
        OrganizationIdentifier,
        RequiredDocument,
        ServiceArea,
        Unit,
        ServiceCapacity,
        URL,
        Taxonomy,
        TaxonomyTerm,
    ]
)
