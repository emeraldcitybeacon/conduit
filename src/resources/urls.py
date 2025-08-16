"""API routes for Resource facade endpoints."""
from django.urls import path

from resources.views.resource import ResourceView
from resources.views.verify import VerifyFieldView
from resources.views.drafts import DraftCreateView, DraftListView
from resources.views.drafts_review import (
    DraftApproveView,
    DraftRejectView,
)
from resources.views.shelves import (
    ShelfListCreateView,
    ShelfDetailView,
    ShelfMemberAddView,
    ShelfMemberRemoveView,
)
from resources.views.bulk_ops import (
    BulkOperationStageView,
    BulkOperationPreviewView,
    BulkOperationCommitView,
    BulkOperationUndoView,
)
from resources.views.search import SearchView

app_name = "resources"

urlpatterns = [
    path("search/", SearchView.as_view(), name="search"),
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
    path("shelves/", ShelfListCreateView.as_view(), name="shelf-list"),
    path("shelves/<uuid:id>/", ShelfDetailView.as_view(), name="shelf-detail"),
    path("shelves/<uuid:id>/add/", ShelfMemberAddView.as_view(), name="shelf-add"),
    path(
        "shelves/<uuid:id>/remove/",
        ShelfMemberRemoveView.as_view(),
        name="shelf-remove",
    ),
    path("bulk-ops/", BulkOperationStageView.as_view(), name="bulk-op-stage"),
    path(
        "bulk-ops/<uuid:id>/preview/",
        BulkOperationPreviewView.as_view(),
        name="bulk-op-preview",
    ),
    path(
        "bulk-ops/<uuid:id>/commit/",
        BulkOperationCommitView.as_view(),
        name="bulk-op-commit",
    ),
    path(
        "bulk-ops/<uuid:id>/undo/",
        BulkOperationUndoView.as_view(),
        name="bulk-op-undo",
    ),
]
