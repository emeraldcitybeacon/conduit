"""Core HSDS models: Organization, Program, Service, and Location."""
from __future__ import annotations

import uuid
from django.db import models


class Organization(models.Model):
    """An organization providing human services."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    alternate_name = models.TextField(blank=True, null=True)
    description = models.TextField()
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    tax_status = models.TextField(blank=True, null=True)
    tax_id = models.TextField(blank=True, null=True)
    year_incorporated = models.PositiveIntegerField(blank=True, null=True)
    legal_status = models.TextField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    uri = models.URLField(blank=True, null=True)
    parent_organization = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="sub_organizations",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name


class Program(models.Model):
    """A program run by an organization."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="programs"
    )
    name = models.TextField()
    alternate_name = models.TextField(blank=True, null=True)
    description = models.TextField()

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name


class Service(models.Model):
    """A specific service offered by an organization or program."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        DEFUNCT = "defunct", "Defunct"
        TEMPORARILY_CLOSED = (
            "temporarily closed",
            "Temporarily Closed",
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="services"
    )
    program = models.ForeignKey(
        Program, on_delete=models.SET_NULL, related_name="services", blank=True, null=True
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, related_name="services", blank=True, null=True)
    name = models.TextField()
    alternate_name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    interpretation_services = models.TextField(blank=True, null=True)
    application_process = models.TextField(blank=True, null=True)
    fees_description = models.TextField(blank=True, null=True)
    wait_time = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    accreditations = models.TextField(blank=True, null=True)
    eligibility_description = models.TextField(blank=True, null=True)
    minimum_age = models.PositiveIntegerField(blank=True, null=True)
    maximum_age = models.PositiveIntegerField(blank=True, null=True)
    assured_date = models.DateField(blank=True, null=True)
    assurer_email = models.EmailField(blank=True, null=True)
    licenses = models.TextField(blank=True, null=True)
    alert = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name


class Location(models.Model):
    """A location where services are available."""

    class LocationType(models.TextChoices):
        PHYSICAL = "physical", "Physical"
        POSTAL = "postal", "Postal"
        VIRTUAL = "virtual", "Virtual"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location_type = models.CharField(max_length=8, choices=LocationType.choices)
    url = models.URLField(blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, related_name="locations", blank=True, null=True
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name="locations", blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    alternate_name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    transportation = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    external_identifier = models.TextField(blank=True, null=True)
    external_identifier_type = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name or str(self.id)
