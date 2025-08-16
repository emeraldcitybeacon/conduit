"""API routes for Resource facade endpoints."""
from django.urls import path

from resources.views.resource import ResourceView
from resources.views.verify import VerifyFieldView

app_name = "resources"

urlpatterns = [
    path("resource/<uuid:id>/", ResourceView.as_view(), name="resource-detail"),
    path(
        "resource/<uuid:id>/verify/",
        VerifyFieldView.as_view(),
        name="resource-verify",
    ),
]
