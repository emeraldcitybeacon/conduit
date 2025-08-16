"""Tests for the Resource API endpoints."""
from __future__ import annotations

import json
from django.contrib.auth import get_user_model
import pytest

from hsds.models import Organization, Location, Service
from hsds_ext.models import FieldVersion

User = get_user_model()


@pytest.fixture
def user_client(client) -> tuple[User, any]:
    """Return a logged-in volunteer client."""

    user = User.objects.create_user(username="vol", password="pw")
    client.login(username="vol", password="pw")
    return user, client


@pytest.fixture
@pytest.mark.django_db
def service() -> Service:
    """Create an organization/location/service trio."""

    org = Organization.objects.create(name="Org", description="d")
    loc = Location.objects.create(location_type="physical", organization=org, name="Loc")
    svc = Service.objects.create(
        organization=org,
        name="Svc",
        description="d",
        status=Service.Status.ACTIVE,
    )
    svc.locations.add(loc)
    return svc


@pytest.mark.django_db
def test_get_resource_returns_composite(user_client, service):
    user, client = user_client
    response = client.get(f"/api/resource/{service.id}/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["service"]["name"] == "Svc"
    assert "ETag" in response.headers


@pytest.mark.django_db
def test_patch_autopublish_field_updates_service(user_client, service):
    user, client = user_client
    # Initial fetch to obtain ETag
    response = client.get(f"/api/resource/{service.id}/")
    etag = response.headers["ETag"]

    data = {"service": {"url": "https://example.com"}}
    response = client.patch(
        f"/api/resource/{service.id}/",
        data=json.dumps(data),
        content_type="application/json",
        HTTP_IF_MATCH=etag,
    )
    assert response.status_code == 200
    service.refresh_from_db()
    assert service.url == "https://example.com"
    # FieldVersion should have been created
    assert FieldVersion.objects.filter(entity_id=service.id, field_path="service.url").exists()


@pytest.mark.django_db
def test_patch_accepts_dotted_form_keys(user_client, service):
    user, client = user_client
    response = client.get(f"/api/resource/{service.id}/")
    etag = response.headers["ETag"]

    response = client.patch(
        f"/api/resource/{service.id}/",
        data={"service.url": "https://example.com/form"},
        HTTP_IF_MATCH=etag,
    )
    assert response.status_code == 200
    service.refresh_from_db()
    assert service.url == "https://example.com/form"


@pytest.mark.django_db
def test_patch_review_required_field_rejected(user_client, service):
    user, client = user_client
    response = client.get(f"/api/resource/{service.id}/")
    etag = response.headers["ETag"]
    data = {"service": {"name": "New"}}
    response = client.patch(
        f"/api/resource/{service.id}/",
        data=json.dumps(data),
        content_type="application/json",
        HTTP_IF_MATCH=etag,
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_patch_version_mismatch_returns_conflict(user_client, service):
    user, client = user_client
    FieldVersion.objects.create(
        entity_type=FieldVersion.EntityType.SERVICE,
        entity_id=service.id,
        field_path="service.url",
        version=2,
        updated_by=user,
    )
    response = client.get(f"/api/resource/{service.id}/")
    etag = response.headers["ETag"]
    data = {"service": {"url": "https://example.com"}, "assert_versions": {"service.url": 1}}
    response = client.patch(
        f"/api/resource/{service.id}/",
        data=json.dumps(data),
        content_type="application/json",
        HTTP_IF_MATCH=etag,
    )
    assert response.status_code == 409
