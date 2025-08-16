"""URL routes for Pulse pages."""
from django.urls import path
from django.views.generic import TemplateView

from .views import components as component_views
from .views import resource as resource_views

app_name = "pulse"

urlpatterns = [
    path("c/<slug:name>/", component_views.component, name="component"),
    path("r/<uuid:id>/", resource_views.ResourceDetailView.as_view(), name="resource-detail"),
    path("r/<uuid:id>/<slug:name>/", resource_views.section, name="resource-section"),
    path("", TemplateView.as_view(template_name="pulse/dashboard.html"), name="home"),
]
