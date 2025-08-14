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
        Program,
        on_delete=models.SET_NULL,
        related_name="services",
        blank=True,
        null=True,
    )
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
    locations = models.ManyToManyField(
        "Location", through="ServiceAtLocation", related_name="services", blank=True
    )

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
        Organization,
        on_delete=models.SET_NULL,
        related_name="locations",
        blank=True,
        null=True,
    )
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


class Accessibility(models.Model):
    """Accessibility features available at a location."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="accessibilities", null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.description or str(self.id)


class Address(models.Model):
    """Postal address for a location."""

    class AddressType(models.TextChoices):
        PHYSICAL = "physical", "Physical"
        POSTAL = "postal", "Postal"
        VIRTUAL = "virtual", "Virtual"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="addresses", null=True, blank=True
    )
    attention = models.TextField(blank=True, null=True)
    address_1 = models.TextField()
    address_2 = models.TextField(blank=True, null=True)
    city = models.TextField()
    region = models.TextField(blank=True, null=True)
    state_province = models.TextField()
    postal_code = models.TextField()
    country = models.TextField()
    address_type = models.CharField(max_length=8, choices=AddressType.choices)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.address_1}, {self.city}"


class ServiceAtLocation(models.Model):
    """Join model linking services and locations."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_at_locations"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="service_at_locations"
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.service} @ {self.location}"


class Contact(models.Model):
    """Contact details for an organization, service, or location."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="contacts", blank=True, null=True
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="contacts", blank=True, null=True
    )
    service_at_location = models.ForeignKey(
        ServiceAtLocation,
        on_delete=models.CASCADE,
        related_name="contacts",
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="contacts", blank=True, null=True
    )
    name = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name or str(self.id)


class Phone(models.Model):
    """Phone numbers for various HSDS entities."""

    class PhoneType(models.TextChoices):
        TEXT = "text", "Text"
        VOICE = "voice", "Voice"
        FAX = "fax", "Fax"
        CELL = "cell", "Cell"
        VIDEO = "video", "Video"
        PAGER = "pager", "Pager"
        TEXTPHONE = "textphone", "Textphone"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="phones", blank=True, null=True
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="phones", blank=True, null=True
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="phones", blank=True, null=True
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="phones", blank=True, null=True
    )
    service_at_location = models.ForeignKey(
        ServiceAtLocation,
        on_delete=models.CASCADE,
        related_name="phones",
        blank=True,
        null=True,
    )
    number = models.TextField()
    extension = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=PhoneType.choices, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.number


class Schedule(models.Model):
    """Opening hours or recurring availability for services and locations."""

    class Weekday(models.TextChoices):
        MO = "MO", "Monday"
        TU = "TU", "Tuesday"
        WE = "WE", "Wednesday"
        TH = "TH", "Thursday"
        FR = "FR", "Friday"
        SA = "SA", "Saturday"
        SU = "SU", "Sunday"

    class Frequency(models.TextChoices):
        WEEKLY = "WEEKLY", "Weekly"
        MONTHLY = "MONTHLY", "Monthly"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="schedules", blank=True, null=True
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="schedules", blank=True, null=True
    )
    service_at_location = models.ForeignKey(
        ServiceAtLocation,
        on_delete=models.CASCADE,
        related_name="schedules",
        blank=True,
        null=True,
    )
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    dtstart = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    until = models.DateField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    wkst = models.CharField(
        max_length=2, choices=Weekday.choices, blank=True, null=True
    )
    freq = models.CharField(
        max_length=7, choices=Frequency.choices, blank=True, null=True
    )
    interval = models.IntegerField(blank=True, null=True)
    byday = models.TextField(blank=True, null=True)
    byweekno = models.TextField(blank=True, null=True)
    bymonthday = models.TextField(blank=True, null=True)
    byyearday = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    opens_at = models.TimeField(blank=True, null=True)
    closes_at = models.TimeField(blank=True, null=True)
    schedule_link = models.URLField(blank=True, null=True)
    attending_type = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.description or str(self.id)


class CostOption(models.Model):
    """Cost and pricing options for a service."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="cost_options"
    )
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    option = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    amount_description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.amount} {self.currency}" if self.amount else str(self.id)


class Funding(models.Model):
    """Funding sources for organizations or services."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="funding", blank=True, null=True
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="funding", blank=True, null=True
    )
    source = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.source or str(self.id)


class Language(models.Model):
    """Languages in which services or communications are available."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="languages", blank=True, null=True
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="languages", blank=True, null=True
    )
    phone = models.ForeignKey(
        "Phone", on_delete=models.CASCADE, related_name="languages", blank=True, null=True
    )
    name = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name or str(self.id)


class OrganizationIdentifier(models.Model):
    """External identifiers for organizations."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="identifiers"
    )
    identifier_scheme = models.TextField(blank=True, null=True)
    identifier_type = models.TextField()
    identifier = models.TextField()

    def __str__(self) -> str:  # pragma: no cover
        return self.identifier


class RequiredDocument(models.Model):
    """Documents required to apply for or receive a service."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="required_documents", blank=True, null=True
    )
    document = models.TextField()
    uri = models.URLField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.document


class ServiceArea(models.Model):
    """Geographic area where a service is available."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_areas", blank=True, null=True
    )
    service_at_location = models.ForeignKey(
        ServiceAtLocation,
        on_delete=models.CASCADE,
        related_name="service_areas",
        blank=True,
        null=True,
    )
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    extent = models.TextField(blank=True, null=True)
    extent_type = models.TextField(blank=True, null=True)
    uri = models.URLField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name or str(self.id)


class Unit(models.Model):
    """Measurement unit for service capacities."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    scheme = models.TextField(blank=True, null=True)
    identifier = models.TextField(blank=True, null=True)
    uri = models.URLField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class ServiceCapacity(models.Model):
    """Capacity information for services."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="capacities"
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="capacities")
    available = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.available}/{self.maximum or '?'} {self.unit}"


class URL(models.Model):
    """Additional URLs for organizations or services."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.TextField(blank=True, null=True)
    url = models.URLField()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="additional_urls", blank=True, null=True
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="additional_urls", blank=True, null=True
    )

    def __str__(self) -> str:  # pragma: no cover
        return self.url


class Taxonomy(models.Model):
    """A taxonomy from which classification terms are drawn."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    uri = models.URLField(blank=True, null=True)
    version = models.TextField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class TaxonomyTerm(models.Model):
    """A term within a taxonomy used to classify services."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField(blank=True, null=True)
    name = models.TextField()
    description = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name="children", blank=True, null=True
    )
    taxonomy = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    taxonomy_object = models.ForeignKey(
        Taxonomy, on_delete=models.CASCADE, related_name="terms", blank=True, null=True
    )
    term_uri = models.URLField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name
