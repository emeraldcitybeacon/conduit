"""Tests for verification event endpoints."""
from __future__ import annotations

import pytest
from django.urls import reverse

from hsds.models import Organization, Service
from hsds_ext.models import VerificationEvent
from users.models import User


@pytest.mark.django_db
def test_verify_checklist_item(client) -> None:
    """Checking a checklist item records a verification event."""
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    client.force_login(user)

    url = reverse("resources:resource-verify", args=[service.id])
    resp = client.post(f"{url}?item=phone")
    assert resp.status_code == 201
    event = VerificationEvent.objects.get()
    assert event.field_path == "service.phones"
    assert event.method == "called"
    assert event.verified_by == user


@pytest.mark.django_db
def test_invalid_checklist_item_returns_400(client) -> None:
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    client.force_login(user)

    url = reverse("resources:resource-verify", args=[service.id])
    resp = client.post(f"{url}?item=unknown")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Unknown checklist item: unknown"
