"""Tests for shelf API endpoints."""
from __future__ import annotations

import uuid

from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_create_and_manage_shelf(client) -> None:
    """User can create a shelf and add/remove members."""

    user = User.objects.create_user(username="alice", password="pw")
    client.force_login(user)

    # Create shelf
    resp = client.post("/api/shelves/", {"name": "My Shelf"})
    assert resp.status_code == 201
    shelf_id = resp.json()["id"]

    # List shelves
    resp = client.get("/api/shelves/")
    assert resp.status_code == 200
    assert any(s["id"] == shelf_id for s in resp.json())

    entity_id = str(uuid.uuid4())
    # Add member
    resp = client.post(
        f"/api/shelves/{shelf_id}/add/",
        {"entity_type": "service", "entity_id": entity_id},
    )
    assert resp.status_code == 201

    # Shelf detail shows member
    resp = client.get(f"/api/shelves/{shelf_id}/")
    assert resp.status_code == 200
    assert resp.json()["members"][0]["entity_id"] == entity_id

    # Remove member
    resp = client.post(
        f"/api/shelves/{shelf_id}/remove/",
        {"entity_type": "service", "entity_id": entity_id},
    )
    assert resp.status_code == 204

    # Confirm member removed
    resp = client.get(f"/api/shelves/{shelf_id}/")
    assert resp.json()["members"] == []

