"""Tests for worklist API endpoints."""
from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from hsds.models import Organization, Service

User = get_user_model()


@pytest.mark.django_db
def test_create_list_and_navigate_worklist(client) -> None:
    """Volunteer can create a worklist and navigate results."""

    user = User.objects.create_user(username="vol", password="pw")
    client.force_login(user)

    org = Organization.objects.create(name="Org", description="d")
    svc1 = Service.objects.create(
        organization=org,
        name="Alpha Service",
        description="d",
        status=Service.Status.ACTIVE,
    )
    svc2 = Service.objects.create(
        organization=org,
        name="Beta Service",
        description="d",
        status=Service.Status.ACTIVE,
    )

    resp = client.post("/api/worklists/", {"name": "List", "query": "Service"})
    assert resp.status_code == 201
    worklist_id = resp.json()["id"]

    resp = client.get("/api/worklists/")
    assert any(w["id"] == worklist_id for w in resp.json())

    resp = client.get(f"/api/worklists/{worklist_id}/next/", {"current": str(svc1.id)})
    assert resp.status_code == 200
    assert resp.json()["id"] == str(svc2.id)
