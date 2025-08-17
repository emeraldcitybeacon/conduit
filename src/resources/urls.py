"""API routes for Resource facade endpoints."""
from django.urls import path

from resources.views.bulk_ops import (
    BulkOperationCommitView,
    BulkOperationPreviewView,
    BulkOperationStageView,
    BulkOperationUndoView,
)
from resources.views.drafts import DraftCreateView, DraftListView
from resources.views.drafts_review import (
    DraftApproveView,
    DraftRejectView,
)
from resources.views.resource import ResourceView
from resources.views.search import SearchView
from resources.views.shelves import (
    ShelfDetailView,
    ShelfListCreateView,
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
from resources.views.merge import MergeView
from resources.views.verify import VerifyFieldView
from resources.views.sensitive import ResourceSensitiveView
from resources.views.siblings import SiblingServiceView
from resources.views.worklists import (
    WorklistDetailView,
    WorklistListCreateView,
    WorklistNavigateView,
    WorklistSearchView,
)

app_name = "resources"

urlpatterns = [
    path("search/", SearchView.as_view(), name="search"),
    path("resource/<uuid:id>/", ResourceView.as_view(), name="resource-detail"),
    path(
        "resource/<uuid:id>/verify/",
        VerifyFieldView.as_view(),
        name="resource-verify",
    ),
    path(
        "resource/<uuid:id>/sensitive/",
        ResourceSensitiveView.as_view(),
        name="resource-sensitive",
    ),
    path(
        "resource/<uuid:id>/siblings/",
        SiblingServiceView.as_view(),
        name="resource-siblings",
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
    path("merge/", MergeView.as_view(), name="merge"),
    path("worklists/", WorklistListCreateView.as_view(), name="worklist-list"),
    path("worklists/<uuid:id>/", WorklistDetailView.as_view(), name="worklist-detail"),
    path(
        "worklists/<uuid:id>/<slug:direction>/",
        WorklistNavigateView.as_view(),
        name="worklist-navigate",
    ),
    path("worklists/search/", WorklistSearchView.as_view(), name="worklist-search"),
]
