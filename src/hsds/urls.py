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
    SearchView,
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
    LocationListView,
    LocationDetailView,
    location_create_view,
    location_edit_view,
    location_address_form_view,
    location_phone_form_view,
    location_schedule_form_view,
    ContactListView,
    ContactDetailView,
    contact_create_view,
    contact_edit_view,
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
    path("manage/search/", SearchView.as_view(), name="search"),
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
    path("manage/locations/", LocationListView.as_view(), name="location-list"),
    path("manage/locations/create/", location_create_view, name="location-create"),
    path("manage/locations/<uuid:pk>/", LocationDetailView.as_view(), name="location-detail"),
    path("manage/locations/<uuid:pk>/edit/", location_edit_view, name="location-edit"),
    path("manage/locations/address-form/", location_address_form_view, name="location-address-form"),
    path("manage/locations/phone-form/", location_phone_form_view, name="location-phone-form"),
    path("manage/locations/schedule-form/", location_schedule_form_view, name="location-schedule-form"),
    path("manage/contacts/", ContactListView.as_view(), name="contact-list"),
    path("manage/contacts/create/", contact_create_view, name="contact-create"),
    path("manage/contacts/<uuid:pk>/", ContactDetailView.as_view(), name="contact-detail"),
    path("manage/contacts/<uuid:pk>/edit/", contact_edit_view, name="contact-edit"),
]
