"""Management views for HSDS organizations and services."""
from __future__ import annotations

from typing import Iterable, Mapping, Type

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from hsds.components.organizations.organization_form import (
    OrganizationForm as OrganizationFormComponent,
)
from hsds.components.services.service_form import (
    ServiceForm as ServiceFormComponent,
)
from hsds.components.services.phone_form import (
    PhoneForm as PhoneFormComponent,
)
from hsds.components.services.schedule_form import (
    ScheduleForm as ScheduleFormComponent,
)
from hsds.components.locations.location_form import (
    LocationForm as LocationFormComponent,
)
from hsds.components.locations.address_form import (
    AddressForm as AddressFormComponent,
)
from hsds.components.contacts.contact_form import (
    ContactForm as ContactFormComponent,
)

from .api import (
    AddressSerializer,
    ContactSerializer,
    LocationSerializer,
    OrganizationSerializer,
    PhoneSerializer,
    ScheduleSerializer,
    ServiceSerializer,
)
from .models import Address, Contact, Location, Organization, Phone, Schedule, Service


def _apply_serializer_errors(form, errors: Mapping[str, Iterable[str]]) -> None:
    """Attach serializer validation errors to a Django form."""

    for field, field_errors in errors.items():
        for error in field_errors:
            form.add_error(field, error)


def _validate_formset(formset, serializer_class: Type[Serializer]) -> bool:
    """Validate each form in a formset using a DRF serializer."""

    valid = True
    for form in formset.forms:
        form.is_valid()  # Populate ``cleaned_data`` for serializer usage.
        form.errors.clear()
        if formset.can_delete and formset._should_delete_form(form):
            continue
        field_names = serializer_class().fields.keys()
        data = {}
        for field in field_names:
            if field not in form.cleaned_data:
                continue
            value = form.cleaned_data.get(field)
            if value in (None, ""):
                continue
            if isinstance(value, models.Model) and not getattr(value, "pk", None):
                continue
            data[field] = value
        try:
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:  # pragma: no cover - exercised via views
            _apply_serializer_errors(form, exc.detail)
            valid = False
    return valid


def _serializer_data(data, serializer_class: Type[Serializer]) -> dict[str, str]:
    """Extract only fields relevant to ``serializer_class`` from ``data``."""

    field_names = serializer_class().fields.keys()
    return {field: data.get(field) for field in field_names if field in data}


def _apply_daisyui_classes(fields: Mapping[str, forms.Field]) -> None:
    """Add daisyUI classes to form fields."""

    for field in fields.values():
        widget = field.widget
        if isinstance(widget, forms.Select):
            classes = "select select-bordered w-full"
        elif isinstance(widget, forms.Textarea):
            classes = "textarea textarea-bordered w-full"
        else:
            classes = "input input-bordered w-full"
        existing = widget.attrs.get("class", "")
        widget.attrs["class"] = f"{existing} {classes}".strip()


class SearchView(LoginRequiredMixin, TemplateView):
    """Perform simple keyword search across core HSDS models."""

    template_name = "hsds/search_results.html"

    def get_context_data(self, **kwargs):
        """Return context with search results for the query string."""

        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        organizations = services = locations = contacts = []
        if query:
            organizations = Organization.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )[:25]
            services = Service.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )[:25]
            locations = Location.objects.filter(name__icontains=query)[:25]
            contacts = Contact.objects.filter(name__icontains=query)[:25]
        context.update(
            {
                "query": query,
                "organizations": organizations,
                "services": services,
                "locations": locations,
                "contacts": contacts,
            }
        )
        return context


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_daisyui_classes(self.fields)


@login_required
def organization_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new organization using DRF serializer validation."""

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        serializer = OrganizationSerializer(
            data=_serializer_data(request.POST, OrganizationSerializer)
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            context = {
                "form": form,
                "action": reverse("hsds:organization-create"),
            }
            return OrganizationFormComponent.render_to_response(
                kwargs=context,
                request=request,
                status=400,
            )
        org = serializer.save()
        if request.headers.get("HX-Request"):
            response = HttpResponse(status=204)
            response["HX-Redirect"] = reverse("hsds:organization-detail", args=[org.pk])
            return response
        return redirect("hsds:organization-detail", pk=org.pk)

    form = OrganizationForm()
    context = {
        "form": form,
        "action": reverse("hsds:organization-create"),
    }
    return OrganizationFormComponent.render_to_response(
        kwargs=context,
        request=request,
    )


@login_required
def organization_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing organization using serializer validation."""

    organization = get_object_or_404(Organization, pk=pk)

    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        serializer = OrganizationSerializer(
            instance=organization,
            data=_serializer_data(request.POST, OrganizationSerializer),
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            context = {
                "form": form,
                "action": reverse("hsds:organization-edit", args=[organization.pk]),
            }
            return OrganizationFormComponent.render_to_response(
                kwargs=context,
                request=request,
                status=400,
            )
        org = serializer.save()
        if request.headers.get("HX-Request"):
            response = HttpResponse(status=204)
            response["HX-Redirect"] = reverse("hsds:organization-detail", args=[org.pk])
            return response
        return redirect("hsds:organization-detail", pk=org.pk)

    form = OrganizationForm(instance=organization)
    context = {
        "form": form,
        "action": reverse("hsds:organization-edit", args=[organization.pk]),
    }
    return OrganizationFormComponent.render_to_response(
        kwargs=context,
        request=request,
    )


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_daisyui_classes(self.fields)


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
        serializer = ServiceSerializer(
            data=_serializer_data(request.POST, ServiceSerializer)
        )
        has_errors = False
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            has_errors = True

        if not _validate_formset(phone_formset, PhoneSerializer):
            has_errors = True
        if not _validate_formset(schedule_formset, ScheduleSerializer):
            has_errors = True

        if not has_errors:
            service = serializer.save()
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
    status_code = 400 if request.method == "POST" else 200
    return ServiceFormComponent.render_to_response(
        kwargs=context,
        request=request,
        status=status_code,
    )


@login_required
def service_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing service and its related phones and schedules."""

    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        phone_formset = PhoneFormSet(request.POST, instance=service, prefix="phones")
        schedule_formset = ScheduleFormSet(request.POST, instance=service, prefix="schedules")
        serializer = ServiceSerializer(
            instance=service,
            data=_serializer_data(request.POST, ServiceSerializer),
        )
        has_errors = False
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            has_errors = True

        if not _validate_formset(phone_formset, PhoneSerializer):
            has_errors = True
        if not _validate_formset(schedule_formset, ScheduleSerializer):
            has_errors = True

        if not has_errors:
            service = serializer.save()
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
    status_code = 400 if request.method == "POST" else 200
    return ServiceFormComponent.render_to_response(
        kwargs=context,
        request=request,
        status=status_code,
    )


@login_required
def phone_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty phone form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = PhoneFormSet(prefix="phones")
    form = formset.empty_form
    form.prefix = f"phones-{form_count}"
    return PhoneFormComponent.render_to_response(
        kwargs={"form": form},
        request=request,
    )


@login_required
def schedule_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty schedule form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = ScheduleFormSet(prefix="schedules")
    form = formset.empty_form
    form.prefix = f"schedules-{form_count}"
    return ScheduleFormComponent.render_to_response(
        kwargs={"form": form},
        request=request,
    )


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_daisyui_classes(self.fields)


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
        serializer = LocationSerializer(
            data=_serializer_data(request.POST, LocationSerializer)
        )
        has_errors = False
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            has_errors = True

        if not _validate_formset(address_formset, AddressSerializer):
            has_errors = True
        if not _validate_formset(phone_formset, PhoneSerializer):
            has_errors = True
        if not _validate_formset(schedule_formset, ScheduleSerializer):
            has_errors = True

        if not has_errors:
            location = serializer.save()
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
    status_code = 400 if request.method == "POST" else 200
    return LocationFormComponent.render_to_response(
        kwargs=context,
        request=request,
        status=status_code,
    )


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
        serializer = LocationSerializer(
            instance=location,
            data=_serializer_data(request.POST, LocationSerializer),
        )
        has_errors = False
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            has_errors = True

        if not _validate_formset(address_formset, AddressSerializer):
            has_errors = True
        if not _validate_formset(phone_formset, PhoneSerializer):
            has_errors = True
        if not _validate_formset(schedule_formset, ScheduleSerializer):
            has_errors = True

        if not has_errors:
            location = serializer.save()
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
    status_code = 400 if request.method == "POST" else 200
    return LocationFormComponent.render_to_response(
        kwargs=context,
        request=request,
        status=status_code,
    )


@login_required
def location_address_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty address form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = AddressFormSet(prefix="addresses")
    form = formset.empty_form
    form.prefix = f"addresses-{form_count}"
    return AddressFormComponent.render_to_response(
        kwargs={"form": form},
        request=request,
    )


@login_required
def location_phone_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty phone form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = LocationPhoneFormSet(prefix="phones")
    form = formset.empty_form
    form.prefix = f"phones-{form_count}"
    return PhoneFormComponent.render_to_response(
        kwargs={"form": form},
        request=request,
    )


@login_required
def location_schedule_form_view(request: HttpRequest) -> HttpResponse:
    """Return a single empty schedule form for dynamic addition via HTMX."""

    form_count = int(request.GET.get("form_count", 0))
    formset = LocationScheduleFormSet(prefix="schedules")
    form = formset.empty_form
    form.prefix = f"schedules-{form_count}"
    return ScheduleFormComponent.render_to_response(
        kwargs={"form": form},
        request=request,
    )


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_daisyui_classes(self.fields)


@login_required
def contact_create_view(request: HttpRequest) -> HttpResponse:
    """Create a new contact using serializer validation."""

    if request.method == "POST":
        form = ContactForm(request.POST)
        serializer = ContactSerializer(
            data=_serializer_data(request.POST, ContactSerializer)
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            context = {"form": form, "action": reverse("hsds:contact-create")}
            return ContactFormComponent.render_to_response(
                kwargs=context,
                request=request,
                status=400,
            )
        contact = serializer.save()
        if request.headers.get("HX-Request"):
            response = HttpResponse(status=204)
            response["HX-Redirect"] = reverse("hsds:contact-detail", args=[contact.pk])
            return response
        return redirect("hsds:contact-detail", pk=contact.pk)

    form = ContactForm()
    context = {"form": form, "action": reverse("hsds:contact-create")}
    return ContactFormComponent.render_to_response(
        kwargs=context,
        request=request,
    )


@login_required
def contact_edit_view(request: HttpRequest, pk: str) -> HttpResponse:
    """Edit an existing contact using serializer validation."""

    contact = get_object_or_404(Contact, pk=pk)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        serializer = ContactSerializer(
            instance=contact,
            data=_serializer_data(request.POST, ContactSerializer),
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            _apply_serializer_errors(form, exc.detail)
            context = {
                "form": form,
                "action": reverse("hsds:contact-edit", args=[contact.pk]),
            }
            return ContactFormComponent.render_to_response(
                kwargs=context,
                request=request,
                status=400,
            )
        contact = serializer.save()
        if request.headers.get("HX-Request"):
            response = HttpResponse(status=204)
            response["HX-Redirect"] = reverse("hsds:contact-detail", args=[contact.pk])
            return response
        return redirect("hsds:contact-detail", pk=contact.pk)

    form = ContactForm(instance=contact)
    context = {
        "form": form,
        "action": reverse("hsds:contact-edit", args=[contact.pk]),
    }
    return ContactFormComponent.render_to_response(
        kwargs=context,
        request=request,
    )
