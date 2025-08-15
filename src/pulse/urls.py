"""URL routes for Pulse pages."""
from django.urls import path
from django.views.generic import TemplateView

app_name = "pulse"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pulse/base.html"), name="home"),
]
