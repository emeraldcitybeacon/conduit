"""Tests for HSDS core models."""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.conduit.settings")
django.setup()
import pytest
from apps.hsds.models import Organization, Program, Service, Location

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
