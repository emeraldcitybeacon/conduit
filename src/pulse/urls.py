"""URL routes for Pulse pages."""
from django.urls import path
from django.views.generic import TemplateView

from .views import components as component_views
from .views import resource as resource_views
from .views import review as review_views
from .views import worklists as worklist_views
from .views import wizard as wizard_views

app_name = "pulse"

urlpatterns = [
    path("c/<slug:name>/", component_views.component, name="component"),
    path("r/<uuid:id>/", resource_views.ResourceDetailView.as_view(), name="resource-detail"),
    path("r/<uuid:id>/<slug:name>/", resource_views.section, name="resource-section"),
    path("new/", wizard_views.WizardStartView.as_view(), name="wizard-start"),
    path("new/org/", wizard_views.OrgStepView.as_view(), name="wizard-org"),
    path("new/location/", wizard_views.LocationStepView.as_view(), name="wizard-location"),
    path("new/service/", wizard_views.ServiceStepView.as_view(), name="wizard-service"),
    path("review/drafts/", review_views.draft_list, name="draft-review-list"),
    path("review/queue/", review_views.change_request_queue, name="change-request-queue"),
    path(
        "review/queue/<uuid:id>/",
        review_views.change_request_detail,
        name="change-request-detail",
    ),
    path(
        "worklists/",
        worklist_views.WorklistIndexView.as_view(),
        name="worklists-index",
    ),
    path("", TemplateView.as_view(template_name="pulse/dashboard.html"), name="home"),
]
