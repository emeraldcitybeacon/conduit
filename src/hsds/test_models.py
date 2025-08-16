"""Tests for HSDS core models."""
import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conduit.settings")
django.setup()

from hsds.models import (  # noqa: E402
    Address,
    Location,
    Organization,
    Phone,
    Program,
    Service,
)


@pytest.mark.django_db
def test_program_belongs_to_organization() -> None:
    """A program should be linked to its organization."""
    org = Organization.objects.create(name="Org", description="Desc")
    program = Program.objects.create(
        name="Prog", description="Program desc", organization=org
    )
    assert program.organization == org


@pytest.mark.django_db
def test_service_links() -> None:
    """Service should reference organization and program."""
    org = Organization.objects.create(name="Org", description="Desc")
    program = Program.objects.create(
        name="Prog", description="Program desc", organization=org
    )
    service = Service.objects.create(
        name="Svc",
        organization=org,
        program=program,
        status=Service.Status.ACTIVE,
    )
    assert service.organization == org
    assert service.program == program


@pytest.mark.django_db
def test_location_association() -> None:
    """Location should optionally belong to an organization."""
    org = Organization.objects.create(name="Org", description="Desc")
    location = Location.objects.create(
        name="Main",
        location_type=Location.LocationType.PHYSICAL,
        organization=org,
    )
    assert location.organization == org


@pytest.mark.django_db
def test_address_links_to_location() -> None:
    """Address should be tied to its location."""
    location = Location.objects.create(
        name="Main",
        location_type=Location.LocationType.PHYSICAL,
    )
    address = Address.objects.create(
        location=location,
        address_1="123 St",
        city="City",
        state_province="State",
        postal_code="12345",
        country="US",
        address_type=Address.AddressType.PHYSICAL,
    )
    assert address.location == location


@pytest.mark.django_db
def test_phone_links_to_organization() -> None:
    """Phone may belong to an organization."""
    org = Organization.objects.create(name="Org", description="Desc")
    phone = Phone.objects.create(number="123", organization=org)
    assert phone.organization == org
