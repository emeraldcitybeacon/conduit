"""Tests for ChangeRequest submission and listing endpoints."""
import pytest
from django.urls import reverse

from hsds.models import Organization, Service
from hsds_ext.models import ChangeRequest
from users.models import User


@pytest.mark.django_db
def test_submit_change_request(client):
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    client.force_login(user)

    patch = [{"op": "replace", "path": "/service/name", "value": "New"}]
    url = reverse("resources:change-request-submit", args=[service.id])
    resp = client.post(url, {"patch": patch, "note": "please"}, content_type="application/json")
    assert resp.status_code == 201
    cr = ChangeRequest.objects.get()
    assert cr.note == "please"
    assert cr.submitted_by == user


@pytest.mark.django_db
def test_list_change_requests(client):
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )
    submitter = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    ChangeRequest.objects.create(
        target_entity_type=ChangeRequest.EntityType.SERVICE,
        target_entity_id=service.id,
        patch=[],
        note="n",
        submitted_by=submitter,
    )
    editor = User.objects.create_user(
        username="ed", password="pw", role=User.Role.EDITOR
    )
    client.force_login(editor)

    url = reverse("resources:change-request-list")
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["note"] == "n"

