"""Tests for the search API endpoint."""
from __future__ import annotations

from typing import Any

import pytest
from django.contrib.auth import get_user_model

from hsds.models import Location, Organization, Phone, Service

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def user_client(client) -> tuple[User, Any]:
    """Return a logged in volunteer client."""

    user = User.objects.create_user(username="vol", password="pw")
    client.login(username="vol", password="pw")
    return user, client


@pytest.mark.django_db
def test_search_by_name_returns_service(user_client) -> None:
    user, client = user_client
    org = Organization.objects.create(name="Alpha Org", description="d")
    loc = Location.objects.create(
        location_type="physical", organization=org, name="Alpha Location"
    )
    svc = Service.objects.create(
        organization=org,
        name="Alpha Service",
        description="d",
        status=Service.Status.ACTIVE,
    )
    svc.locations.add(loc)

    resp = client.get("/api/search/", {"q": "Alpha"})
    assert resp.status_code == 200
    payload = resp.json()["results"]
    assert any(r["id"] == str(svc.id) for r in payload)


@pytest.mark.django_db
def test_search_by_phone_returns_service(user_client) -> None:
    user, client = user_client
    org = Organization.objects.create(name="Beta Org", description="d")
    svc = Service.objects.create(
        organization=org,
        name="Beta Service",
        description="d",
        status=Service.Status.ACTIVE,
    )
    Phone.objects.create(service=svc, number="555-1234")

    resp = client.get("/api/search/", {"q": "555"})
    assert resp.status_code == 200
    payload = resp.json()["results"]
    assert any(r["id"] == str(svc.id) and r.get("phone") == "555-1234" for r in payload)
