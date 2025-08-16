"""API routes for Resource facade endpoints."""
from django.urls import path

from resources.views.resource import ResourceView
from resources.views.verify import VerifyFieldView
from resources.views.drafts import DraftCreateView, DraftListView
from resources.views.drafts_review import (
    DraftApproveView,
    DraftRejectView,
)

app_name = "resources"

urlpatterns = [
    path("resource/<uuid:id>/", ResourceView.as_view(), name="resource-detail"),
    path(
        "resource/<uuid:id>/verify/",
        VerifyFieldView.as_view(),
        name="resource-verify",
    ),
    path("resource/", DraftCreateView.as_view(), name="resource-create"),
    path("drafts/", DraftListView.as_view(), name="draft-list"),
    path(
        "drafts/<uuid:id>/approve/",
        DraftApproveView.as_view(),
        name="draft-approve",
    ),
    path(
        "drafts/<uuid:id>/reject/",
        DraftRejectView.as_view(),
        name="draft-reject",
    ),
]
