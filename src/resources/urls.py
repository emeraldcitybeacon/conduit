"""API routes for Resource facade endpoints."""
from django.urls import path

from resources.views.resource import ResourceView

app_name = "resources"

urlpatterns = [
    path("resource/<uuid:id>/", ResourceView.as_view(), name="resource-detail"),
]
