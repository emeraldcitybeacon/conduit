"""Model translations for HSDS models."""
from modeltranslation.translator import TranslationOptions, register

from .models import (
    Accessibility,
    Contact,
    CostOption,
    Location,
    Organization,
    Program,
    Service,
    ServiceArea,
    Taxonomy,
    TaxonomyTerm,
)


@register(Organization)
class OrganizationTR(TranslationOptions):
    """Translatable fields for Organization."""
    fields = ("name", "alternate_name", "description")


@register(Program)
class ProgramTR(TranslationOptions):
    """Translatable fields for Program."""
    fields = ("name", "alternate_name", "description")


@register(Service)
class ServiceTR(TranslationOptions):
    """Translatable fields for Service."""
    fields = (
        "name",
        "alternate_name",
        "description",
        "interpretation_services",
        "application_process",
        "fees_description",
        "wait_time",
        "fees",
        "accreditations",
        "eligibility_description",
        "alert",
    )


@register(Location)
class LocationTR(TranslationOptions):
    """Translatable fields for Location."""
    fields = ("name", "alternate_name", "description", "transportation")


@register(Contact)
class ContactTR(TranslationOptions):
    """Translatable fields for Contact."""
    fields = ("name", "title", "department")


@register(Accessibility)
class AccessibilityTR(TranslationOptions):
    """Translatable fields for Accessibility."""
    fields = ("description", "details")


@register(CostOption)
class CostOptionTR(TranslationOptions):
    """Translatable fields for CostOption."""
    fields = ("option", "amount_description")


@register(ServiceArea)
class ServiceAreaTR(TranslationOptions):
    """Translatable fields for ServiceArea."""
    fields = ("name", "description", "extent", "extent_type")


@register(Taxonomy)
class TaxonomyTR(TranslationOptions):
    """Translatable fields for Taxonomy."""
    fields = ("name", "description")


@register(TaxonomyTerm)
class TaxonomyTermTR(TranslationOptions):
    """Translatable fields for TaxonomyTerm."""
    fields = ("name", "description")
