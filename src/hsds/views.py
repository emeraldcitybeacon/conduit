"""HTMX-enabled views for managing HSDS data."""
from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .forms import OrganizationForm
from .models import Organization


class OrganizationListView(LoginRequiredMixin, ListView):
    """Display a list of organizations."""

    model = Organization
    template_name = "hsds/organization_list.html"
    context_object_name = "organizations"


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    """Display details for a single organization."""

    model = Organization
    template_name = "hsds/organization_detail.html"
    context_object_name = "organization"


@login_required
def organization_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new :class:`Organization` instance."""

    form = OrganizationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        organization = form.save()
        if request.headers.get("HX-Request"):
            response = HttpResponse()
            response.headers["HX-Redirect"] = reverse(
                "hsds:organization-detail", args=[organization.pk]
            )
            return response
        return redirect("hsds:organization-detail", pk=organization.pk)

    if request.headers.get("HX-Request"):
        from conduit.components.hsds.organization_form import (
            OrganizationForm as OrganizationFormComponent,
        )

        return OrganizationFormComponent.render_to_response(
            request=request,
            kwargs={"form": form},
        )

    return render(
        request,
        "hsds/organization_detail.html",
        {"organization": None, "form": form},
    )


@login_required
def organization_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing :class:`Organization` instance."""

    organization = get_object_or_404(Organization, pk=pk)
    form = OrganizationForm(request.POST or None, instance=organization)

    if request.method == "POST" and form.is_valid():
        form.save()
        if request.headers.get("HX-Request"):
            response = HttpResponse()
            response.headers["HX-Redirect"] = reverse(
                "hsds:organization-detail", args=[organization.pk]
            )
            return response
        return redirect("hsds:organization-detail", pk=organization.pk)

    if request.headers.get("HX-Request"):
        from conduit.components.hsds.organization_form import (
            OrganizationForm as OrganizationFormComponent,
        )

        return OrganizationFormComponent.render_to_response(
            request=request,
            kwargs={"form": form},
        )

    return render(
        request,
        "hsds/organization_detail.html",
        {"organization": organization, "form": form},
    )
