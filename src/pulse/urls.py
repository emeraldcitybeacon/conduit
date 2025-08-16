"""URL routes for Pulse pages."""
from django.urls import path
from django.views.generic import TemplateView

from .views import components as component_views

app_name = "pulse"

urlpatterns = [
    path("c/<slug:name>/", component_views.component, name="component"),
    path("", TemplateView.as_view(template_name="pulse/base.html"), name="home"),
]
