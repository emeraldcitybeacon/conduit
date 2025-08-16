"""Tests for draft resource API endpoints."""
from __future__ import annotations

import json

from django.contrib.auth import get_user_model
import pytest

from hsds_ext.models import DraftResource

User = get_user_model()


@pytest.fixture
def user_client(client) -> tuple[User, any]:
    """Return a logged-in volunteer client."""

    user = User.objects.create_user(username="vol", password="pw")
    client.login(username="vol", password="pw")
    return user, client


@pytest.mark.django_db
def test_post_creates_draft(user_client):
    user, client = user_client
    payload = {
        "organization": {"name": "Org"},
        "location": {"name": "Loc"},
        "service": {"name": "Svc"},
    }
    response = client.post(
        "/api/resource/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 201
    draft = DraftResource.objects.first()
    assert draft is not None
    assert draft.payload["organization"]["name"] == "Org"


@pytest.mark.django_db
def test_get_lists_user_drafts(user_client):
    user, client = user_client
    DraftResource.objects.create(created_by=user, payload={"foo": "bar"})
    response = client.get("/api/drafts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == DraftResource.Status.DRAFT
