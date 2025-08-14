"""URL routing for the HSDS app."""

from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .api import (
    LocationViewSet,
    OrganizationViewSet,
    ProgramViewSet,
    ServiceViewSet,
)


api_router = DefaultRouter()
api_router.register(r"organizations", OrganizationViewSet)
api_router.register(r"programs", ProgramViewSet)
api_router.register(r"services", ServiceViewSet)
api_router.register(r"locations", LocationViewSet)


# Placeholder for future non-API URL patterns (e.g., HTMX views).
urlpatterns: list = []

