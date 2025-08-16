"""Tests for draft resource API endpoints."""
from __future__ import annotations

import json

from django.contrib.auth import get_user_model
import pytest

from hsds.models import Service
from hsds_ext.models import DraftResource, FieldVersion, VerificationEvent

User = get_user_model()


@pytest.fixture
def user_client(client) -> tuple[User, any]:
    """Return a logged-in volunteer client."""

    user = User.objects.create_user(username="vol", password="pw")
    client.login(username="vol", password="pw")
    return user, client


@pytest.fixture
def editor_client(client) -> tuple[User, any]:
    """Return a logged-in editor client."""

    user = User.objects.create_user(
        username="ed", password="pw", role=User.Role.EDITOR
    )
    client.login(username="ed", password="pw")
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


@pytest.mark.django_db
def test_editor_can_approve_draft(editor_client):
    editor, client = editor_client
    volunteer = User.objects.create_user(username="vol2", password="pw")
    payload = {
        "organization": {"name": "Org", "description": "Desc"},
        "location": {"name": "Loc", "location_type": "physical"},
        "service": {"name": "Svc", "status": "active"},
    }
    draft = DraftResource.objects.create(created_by=volunteer, payload=payload)
    response = client.post(f"/api/drafts/{draft.id}/approve/")
    assert response.status_code == 200
    draft.refresh_from_db()
    assert draft.status == DraftResource.Status.APPROVED
    service = Service.objects.get(name="Svc")
    fv_exists = FieldVersion.objects.filter(
        entity_type=FieldVersion.EntityType.SERVICE,
        entity_id=service.id,
        field_path="service.name",
    ).exists()
    assert fv_exists
    ve_exists = VerificationEvent.objects.filter(
        entity_type=VerificationEvent.EntityType.SERVICE,
        entity_id=service.id,
        field_path="service.name",
    ).exists()
    assert ve_exists


@pytest.mark.django_db
def test_editor_can_reject_draft(editor_client):
    editor, client = editor_client
    volunteer = User.objects.create_user(username="vol3", password="pw")
    payload = {
        "organization": {"name": "Org", "description": "Desc"},
        "location": {"name": "Loc", "location_type": "physical"},
        "service": {"name": "Svc", "status": "active"},
    }
    draft = DraftResource.objects.create(created_by=volunteer, payload=payload)
    response = client.post(
        f"/api/drafts/{draft.id}/reject/", {"note": "bad"}
    )
    assert response.status_code == 200
    draft.refresh_from_db()
    assert draft.status == DraftResource.Status.REJECTED
    assert draft.review_note == "bad"
    assert Service.objects.filter(name="Svc").count() == 0
