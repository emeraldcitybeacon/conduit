"""API tests for HSDS core endpoints."""

from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from hsds.models import Address, Location, Organization, Service, ServiceAtLocation


@pytest.mark.django_db
def test_organization_list_endpoint_returns_created_organization() -> None:
    """Ensure the organization list API returns persisted objects."""

    org = Organization.objects.create(
        name="Test Org",
        description="Desc",
    )

    client = APIClient()
    url = reverse("organization-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data[0]["id"] == str(org.id)


@pytest.mark.django_db
def test_address_list_endpoint_returns_created_address() -> None:
    """Ensure the address list API returns persisted objects."""

    location = Location.objects.create(location_type="physical")
    addr = Address.objects.create(
        location=location,
        address_1="123 Main St",
        city="Town",
        state_province="State",
        postal_code="12345",
        country="Country",
        address_type="physical",
    )

    client = APIClient()
    url = reverse("address-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data[0]["id"] == str(addr.id)


@pytest.mark.django_db
def test_service_detail_returns_nested_location_address() -> None:
    """Service detail should include nested location and address data."""

    org = Organization.objects.create(name="Org", description="Desc")
    service = Service.objects.create(
        organization=org,
        name="Svc",
        status=Service.Status.ACTIVE,
    )
    location = Location.objects.create(location_type="physical")
    Address.objects.create(
        location=location,
        address_1="123 Main St",
        city="Town",
        state_province="State",
        postal_code="12345",
        country="Country",
        address_type="physical",
    )
    ServiceAtLocation.objects.create(service=service, location=location)

    client = APIClient()
    url = reverse("service-detail", args=[service.id])
    response = client.get(url)

    assert response.status_code == 200
    nested_address = response.data["service_at_locations"][0]["location"]["addresses"][0]
    assert nested_address["address_1"] == "123 Main St"

