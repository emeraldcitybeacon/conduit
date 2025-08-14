"""HTMX management views for HSDS models."""

from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .models import Organization


class OrganizationForm(ModelForm):
    """Form used to create and update ``Organization`` instances."""

    class Meta:
        model = Organization
        fields = ["name", "alternate_name", "description", "email", "website"]


class OrganizationListView(LoginRequiredMixin, ListView):
    """Display a table of organizations."""

    model = Organization
    template_name = "hsds/organization_list.html"
    context_object_name = "organizations"
    ordering = ["name"]


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    """Show details for a single organization."""

    model = Organization
    template_name = "hsds/organization_detail.html"
    context_object_name = "organization"


@login_required
def organization_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new organization via an HTMX-enabled form."""

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:organization_detail", args=[org.pk]
                )
                return response
            return redirect("hsds:organization_detail", pk=org.pk)
    else:
        form = OrganizationForm()

    return render(
        request,
        "hsds/includes/organization_form.html",
        {"form": form, "action": reverse("hsds:organization_create")},
    )


@login_required
def organization_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing organization via an HTMX-enabled form."""

    organization = get_object_or_404(Organization, pk=pk)
    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            org = form.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:organization_detail", args=[org.pk]
                )
                return response
            return redirect("hsds:organization_detail", pk=org.pk)
    else:
        form = OrganizationForm(instance=organization)

    return render(
        request,
        "hsds/includes/organization_form.html",
        {
            "form": form,
            "action": reverse("hsds:organization_edit", args=[organization.pk]),
        },
    )
