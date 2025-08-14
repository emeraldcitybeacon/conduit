"""URL routing for the HSDS app."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .api import (
    AccessibilityViewSet,
    AddressViewSet,
    ContactViewSet,
    CostOptionViewSet,
    FundingViewSet,
    LanguageViewSet,
    LocationViewSet,
    OrganizationIdentifierViewSet,
    OrganizationViewSet,
    ProgramViewSet,
    RequiredDocumentViewSet,
    ScheduleViewSet,
    ServiceAreaViewSet,
    ServiceAtLocationViewSet,
    ServiceCapacityViewSet,
    ServiceViewSet,
    TaxonomyTermViewSet,
    TaxonomyViewSet,
    URLViewSet,
    UnitViewSet,
    PhoneViewSet,
)


api_router = DefaultRouter()
api_router.register(r"organizations", OrganizationViewSet)
api_router.register(r"programs", ProgramViewSet)
api_router.register(r"services", ServiceViewSet)
api_router.register(r"locations", LocationViewSet)
api_router.register(r"accessibilities", AccessibilityViewSet)
api_router.register(r"addresses", AddressViewSet)
api_router.register(r"contacts", ContactViewSet)
api_router.register(r"phones", PhoneViewSet)
api_router.register(r"schedules", ScheduleViewSet)
api_router.register(r"service-at-locations", ServiceAtLocationViewSet)
api_router.register(r"service-areas", ServiceAreaViewSet)
api_router.register(r"cost-options", CostOptionViewSet)
api_router.register(r"funding", FundingViewSet)
api_router.register(r"languages", LanguageViewSet)
api_router.register(r"organization-identifiers", OrganizationIdentifierViewSet)
api_router.register(r"required-documents", RequiredDocumentViewSet)
api_router.register(r"units", UnitViewSet)
api_router.register(r"service-capacities", ServiceCapacityViewSet)
api_router.register(r"urls", URLViewSet)
api_router.register(r"taxonomies", TaxonomyViewSet)
api_router.register(r"taxonomy-terms", TaxonomyTermViewSet)


# Placeholder for future non-API URL patterns (e.g., HTMX views).
urlpatterns: list = []

