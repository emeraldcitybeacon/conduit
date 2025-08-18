"""Tests for Pulse resource views."""
from __future__ import annotations

import uuid

import pytest
from django.urls import reverse

from hsds.models import Location, Organization, Service, ServiceAtLocation


@pytest.mark.django_db
def test_home_view(client) -> None:
    """The data health dashboard loads successfully."""

    resp = client.get(reverse("pulse:dashboard"))
    assert resp.status_code == 200
    assert b"Pulse Dashboard" in resp.content


@pytest.mark.django_db
def test_resource_detail_view(client):
    """The resource detail view renders for an existing service."""

    org = Organization.objects.create(id=uuid.uuid4(), name="Org")
    location = Location.objects.create(id=uuid.uuid4(), organization=org, location_type="physical")
    service = Service.objects.create(id=uuid.uuid4(), organization=org, name="Svc", status="active")
    ServiceAtLocation.objects.create(service=service, location=location)

    url = reverse("pulse:resource-detail", args=[service.id])
    resp = client.get(url)
    assert resp.status_code == 200
    assert b"Svc" in resp.content
