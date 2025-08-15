"""Management views for HSDS organizations and services."""
from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, inlineformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .models import (
    Organization,
    Service,
    Phone,
    Schedule,
    Location,
    Address,
    Contact,
)


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


class ServiceListView(LoginRequiredMixin, ListView):
    """Display a list of services."""

    model = Service
    template_name = "hsds/service_list.html"
    context_object_name = "services"

    def get_queryset(self):  # pragma: no cover - simple ordering
        return Service.objects.order_by("name")


class ServiceDetailView(LoginRequiredMixin, DetailView):
    """Display details for a single service."""

    model = Service
    template_name = "hsds/service_detail.html"
    context_object_name = "service"


class ServiceForm(ModelForm):
    """Form for creating and editing services."""

    class Meta:
        model = Service
        fields = ["organization", "name", "description", "status", "email"]


PhoneFormSet = inlineformset_factory(
    Service,
    Phone,
    fields=["number", "type", "extension", "description"],
    extra=0,
    can_delete=True,
    )

ScheduleFormSet = inlineformset_factory(
    Service,
    Schedule,
    fields=["description", "opens_at", "closes_at", "valid_from", "valid_to"],
    extra=0,
    can_delete=True,
    )


@login_required
def service_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new service with nested phone and schedule forms."""

    if request.method == "POST":
        form = ServiceForm(request.POST)
        phone_formset = PhoneFormSet(request.POST, prefix="phones")
        schedule_formset = ScheduleFormSet(request.POST, prefix="schedules")
        if form.is_valid() and phone_formset.is_valid() and schedule_formset.is_valid():
            service = form.save()
            phone_formset.instance = service
            schedule_formset.instance = service
            phone_formset.save()
            schedule_formset.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse("hsds:service-detail", args=[service.pk])
                return response
            return redirect("hsds:service-detail", pk=service.pk)
    else:
        form = ServiceForm()
        phone_formset = PhoneFormSet(prefix="phones")
        schedule_formset = ScheduleFormSet(prefix="schedules")

    context = {
        "form": form,
        "phone_formset": phone_formset,
        "schedule_formset": schedule_formset,
        "action": reverse("hsds:service-create"),
    }
    return render(request, "hsds/includes/service_form.html", context)


@login_required
def service_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing service and its related phones and schedules."""

    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        phone_formset = PhoneFormSet(request.POST, instance=service, prefix="phones")
        schedule_formset = ScheduleFormSet(request.POST, instance=service, prefix="schedules")
        if form.is_valid() and phone_formset.is_valid() and schedule_formset.is_valid():
            service = form.save()
            phone_formset.save()
            schedule_formset.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse("hsds:service-detail", args=[service.pk])
                return response
            return redirect("hsds:service-detail", pk=service.pk)
    else:
        form = ServiceForm(instance=service)
        phone_formset = PhoneFormSet(instance=service, prefix="phones")
        schedule_formset = ScheduleFormSet(instance=service, prefix="schedules")

    context = {
        "form": form,
        "phone_formset": phone_formset,
        "schedule_formset": schedule_formset,
        "action": reverse("hsds:service-edit", args=[service.pk]),
    }
    return render(request, "hsds/includes/service_form.html", context)


@login_required
def phone_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty phone form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = PhoneFormSet(prefix="phones")
    form = formset.empty_form
    form.prefix = f"phones-{form_count}"
    return render(request, "hsds/includes/phone_form.html", {"form": form})


@login_required
def schedule_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty schedule form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = ScheduleFormSet(prefix="schedules")
    form = formset.empty_form
    form.prefix = f"schedules-{form_count}"
    return render(request, "hsds/includes/schedule_form.html", {"form": form})


class LocationListView(LoginRequiredMixin, ListView):
    """Display a list of locations."""

    model = Location
    template_name = "hsds/location_list.html"
    context_object_name = "locations"

    def get_queryset(self):  # pragma: no cover - simple ordering
        return Location.objects.order_by("name")


class LocationDetailView(LoginRequiredMixin, DetailView):
    """Display details for a single location."""

    model = Location
    template_name = "hsds/location_detail.html"
    context_object_name = "location"


class LocationForm(ModelForm):
    """Form for creating and editing locations."""

    class Meta:
        model = Location
        fields = [
            "organization",
            "location_type",
            "name",
            "description",
            "latitude",
            "longitude",
        ]


AddressFormSet = inlineformset_factory(
    Location,
    Address,
    fields=[
        "attention",
        "address_1",
        "address_2",
        "city",
        "state_province",
        "postal_code",
        "country",
        "address_type",
    ],
    extra=0,
    can_delete=True,
)


LocationPhoneFormSet = inlineformset_factory(
    Location,
    Phone,
    fields=["number", "type", "extension", "description"],
    extra=0,
    can_delete=True,
)


LocationScheduleFormSet = inlineformset_factory(
    Location,
    Schedule,
    fields=["description", "opens_at", "closes_at", "valid_from", "valid_to"],
    extra=0,
    can_delete=True,
)


@login_required
def location_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new location with nested address, phone, and schedule forms."""

    if request.method == "POST":
        form = LocationForm(request.POST)
        address_formset = AddressFormSet(request.POST, prefix="addresses")
        phone_formset = LocationPhoneFormSet(request.POST, prefix="phones")
        schedule_formset = LocationScheduleFormSet(request.POST, prefix="schedules")
        if (
            form.is_valid()
            and address_formset.is_valid()
            and phone_formset.is_valid()
            and schedule_formset.is_valid()
        ):
            location = form.save()
            address_formset.instance = location
            phone_formset.instance = location
            schedule_formset.instance = location
            address_formset.save()
            phone_formset.save()
            schedule_formset.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:location-detail", args=[location.pk]
                )
                return response
            return redirect("hsds:location-detail", pk=location.pk)
    else:
        form = LocationForm()
        address_formset = AddressFormSet(prefix="addresses")
        phone_formset = LocationPhoneFormSet(prefix="phones")
        schedule_formset = LocationScheduleFormSet(prefix="schedules")

    context = {
        "form": form,
        "address_formset": address_formset,
        "phone_formset": phone_formset,
        "schedule_formset": schedule_formset,
        "action": reverse("hsds:location-create"),
    }
    return render(request, "hsds/includes/location_form.html", context)


@login_required
def location_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing location and its related addresses, phones, and schedules."""

    location = get_object_or_404(Location, pk=pk)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        address_formset = AddressFormSet(
            request.POST, instance=location, prefix="addresses"
        )
        phone_formset = LocationPhoneFormSet(
            request.POST, instance=location, prefix="phones"
        )
        schedule_formset = LocationScheduleFormSet(
            request.POST, instance=location, prefix="schedules"
        )
        if (
            form.is_valid()
            and address_formset.is_valid()
            and phone_formset.is_valid()
            and schedule_formset.is_valid()
        ):
            location = form.save()
            address_formset.save()
            phone_formset.save()
            schedule_formset.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:location-detail", args=[location.pk]
                )
                return response
            return redirect("hsds:location-detail", pk=location.pk)
    else:
        form = LocationForm(instance=location)
        address_formset = AddressFormSet(instance=location, prefix="addresses")
        phone_formset = LocationPhoneFormSet(instance=location, prefix="phones")
        schedule_formset = LocationScheduleFormSet(
            instance=location, prefix="schedules"
        )

    context = {
        "form": form,
        "address_formset": address_formset,
        "phone_formset": phone_formset,
        "schedule_formset": schedule_formset,
        "action": reverse("hsds:location-edit", args=[location.pk]),
    }
    return render(request, "hsds/includes/location_form.html", context)


@login_required
def location_address_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty address form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = AddressFormSet(prefix="addresses")
    form = formset.empty_form
    form.prefix = f"addresses-{form_count}"
    return render(request, "hsds/includes/address_form.html", {"form": form})


@login_required
def location_phone_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty phone form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = LocationPhoneFormSet(prefix="phones")
    form = formset.empty_form
    form.prefix = f"phones-{form_count}"
    return render(request, "hsds/includes/phone_form.html", {"form": form})


@login_required
def location_schedule_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty schedule form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = LocationScheduleFormSet(prefix="schedules")
    form = formset.empty_form
    form.prefix = f"schedules-{form_count}"
    return render(request, "hsds/includes/schedule_form.html", {"form": form})


class ContactListView(LoginRequiredMixin, ListView):
    """Display a list of contacts."""

    model = Contact
    template_name = "hsds/contact_list.html"
    context_object_name = "contacts"

    def get_queryset(self):  # pragma: no cover - simple ordering
        return Contact.objects.order_by("name")


class ContactDetailView(LoginRequiredMixin, DetailView):
    """Display details for a single contact."""

    model = Contact
    template_name = "hsds/contact_detail.html"
    context_object_name = "contact"


class ContactForm(ModelForm):
    """Form for creating and editing contacts."""

    class Meta:
        model = Contact
        fields = ["organization", "service", "location", "name", "title", "email"]


@login_required
def contact_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new contact."""

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:contact-detail", args=[contact.pk]
                )
                return response
            return redirect("hsds:contact-detail", pk=contact.pk)
    else:
        form = ContactForm()

    context = {"form": form, "action": reverse("hsds:contact-create")}
    return render(request, "hsds/includes/contact_form.html", context)


@login_required
def contact_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing contact."""

    contact = get_object_or_404(Contact, pk=pk)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse(
                    "hsds:contact-detail", args=[contact.pk]
                )
                return response
            return redirect("hsds:contact-detail", pk=contact.pk)
    else:
        form = ContactForm(instance=contact)

    context = {
        "form": form,
        "action": reverse("hsds:contact-edit", args=[contact.pk]),
    }
    return render(request, "hsds/includes/contact_form.html", context)
