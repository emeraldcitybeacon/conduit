"""Management views for HSDS organizations."""
from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .models import Organization


class OrganizationListView(LoginRequiredMixin, ListView):
    """Display a list of organizations."""

    model = Organization
    template_name = "hsds/organization_list.html"
    context_object_name = "organizations"

    def get_queryset(self):  # pragma: no cover - simple ordering
        return Organization.objects.order_by("name")


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    """Display details for a single organization."""

    model = Organization
    template_name = "hsds/organization_detail.html"
    context_object_name = "organization"


class OrganizationForm(ModelForm):
    """Form for creating and editing organizations."""

    class Meta:
        model = Organization
        fields = ["name", "description", "email", "website"]


@login_required
def organization_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new organization."""

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:organization-detail", args=[org.pk]
                )
                return response
            return redirect("hsds:organization-detail", pk=org.pk)
    else:
        form = OrganizationForm()

    context = {
        "form": form,
        "action": reverse("hsds:organization-create"),
    }
    return render(request, "hsds/includes/organization_form.html", context)


@login_required
def organization_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing organization."""

    organization = get_object_or_404(Organization, pk=pk)

    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            org = form.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:organization-detail", args=[org.pk]
                )
                return response
            return redirect("hsds:organization-detail", pk=org.pk)
    else:
        form = OrganizationForm(instance=organization)

    context = {
        "form": form,
        "action": reverse("hsds:organization-edit", args=[organization.pk]),
    }
    return render(request, "hsds/includes/organization_form.html", context)
