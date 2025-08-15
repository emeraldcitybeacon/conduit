"""URL routing for the HSDS app."""

from __future__ import annotations

from django.urls import path
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
from .views import (
    OrganizationDetailView,
    OrganizationListView,
    organization_create_view,
    organization_edit_view,
    ServiceDetailView,
    ServiceListView,
    service_create_view,
    service_edit_view,
    phone_form_view,
    schedule_form_view,
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

app_name = "hsds"

urlpatterns = [
    path("manage/organizations/", OrganizationListView.as_view(), name="organization-list"),
    path("manage/organizations/create/", organization_create_view, name="organization-create"),
    path("manage/organizations/<uuid:pk>/", OrganizationDetailView.as_view(), name="organization-detail"),
    path("manage/organizations/<uuid:pk>/edit/", organization_edit_view, name="organization-edit"),
    path("manage/services/", ServiceListView.as_view(), name="service-list"),
    path("manage/services/create/", service_create_view, name="service-create"),
    path("manage/services/<uuid:pk>/", ServiceDetailView.as_view(), name="service-detail"),
    path("manage/services/<uuid:pk>/edit/", service_edit_view, name="service-edit"),
    path("manage/services/phone-form/", phone_form_view, name="phone-form"),
    path("manage/services/schedule-form/", schedule_form_view, name="schedule-form"),
]
