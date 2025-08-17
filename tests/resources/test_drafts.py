"""Tests for Draft resource workflow."""
from __future__ import annotations

import json

import pytest
from django.urls import reverse

from hsds.models import Service
from hsds_ext.models import DraftResource, FieldVersion, VerificationEvent
from users.models import User


@pytest.fixture
def volunteer_client(client):
    user = User.objects.create_user(username="vol", password="pw")
    client.force_login(user)
    return user, client


@pytest.fixture
def editor_client(client):
    user = User.objects.create_user(username="ed", password="pw", role=User.Role.EDITOR)
    client.force_login(user)
    return user, client


@pytest.mark.django_db
def test_post_creates_draft(volunteer_client):
    user, client = volunteer_client
    payload = {
        "organization": {"name": "Org"},
        "location": {"name": "Loc"},
        "service": {"name": "Svc"},
    }
    resp = client.post(reverse("resources:resource-create"), data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    draft = DraftResource.objects.get()
    assert draft.created_by == user
    assert draft.payload["service"]["name"] == "Svc"


@pytest.mark.django_db
def test_editor_can_approve_draft(editor_client):
    editor, client = editor_client
    volunteer = User.objects.create_user(username="v2", password="pw")
    payload = {
        "organization": {"name": "Org", "description": "d"},
        "location": {"name": "Loc", "location_type": "physical"},
        "service": {"name": "Svc", "status": "active"},
    }
    draft = DraftResource.objects.create(created_by=volunteer, payload=payload)
    resp = client.post(reverse("resources:draft-approve", args=[draft.id]))
    assert resp.status_code == 200
    draft.refresh_from_db()
    assert draft.status == DraftResource.Status.APPROVED
    service = Service.objects.get(name="Svc")
    assert FieldVersion.objects.filter(entity_id=service.id, field_path="service.name").exists()
    assert VerificationEvent.objects.filter(entity_id=service.id, field_path="service.name").exists()


@pytest.mark.django_db
def test_editor_can_reject_draft(editor_client):
    editor, client = editor_client
    volunteer = User.objects.create_user(username="v3", password="pw")
    payload = {
        "organization": {"name": "Org", "description": "d"},
        "location": {"name": "Loc", "location_type": "physical"},
        "service": {"name": "Svc", "status": "active"},
    }
    draft = DraftResource.objects.create(created_by=volunteer, payload=payload)
    resp = client.post(reverse("resources:draft-reject", args=[draft.id]), {"note": "bad"})
    assert resp.status_code == 200
    draft.refresh_from_db()
    assert draft.status == DraftResource.Status.REJECTED
    assert draft.review_note == "bad"
    assert Service.objects.filter(name="Svc").count() == 0
