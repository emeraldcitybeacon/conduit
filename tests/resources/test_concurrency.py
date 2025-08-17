"""Tests for optimistic concurrency responses."""
import json

import pytest
from django.urls import reverse

from hsds.models import Organization, Service
from hsds_ext.models import FieldVersion
from users.models import User


@pytest.mark.django_db
def test_patch_precondition_failed_returns_current_and_etags(client):
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(organization=org, name="Svc", status=Service.Status.ACTIVE, url="http://old")
    user = User.objects.create_user(username="vol", password="pw", role=User.Role.VOLUNTEER)
    client.force_login(user)

    FieldVersion.objects.create(
        entity_type=FieldVersion.EntityType.SERVICE,
        entity_id=service.id,
        field_path="service.url",
        version=1,
        updated_by=user,
    )
    resp = client.get(reverse("resources:resource-detail", args=[service.id]))
    etag = resp.headers["ETag"]

    fv = FieldVersion.objects.get(field_path="service.url")
    fv.version = 2
    fv.save()
    service.url = "http://current"
    service.save(update_fields=["url"])

    data = {"service": {"url": "http://mine"}, "assert_versions": {"service.url": 1}}
    resp = client.patch(
        reverse("resources:resource-detail", args=[service.id]),
        data=json.dumps(data),
        content_type="application/json",
        HTTP_IF_MATCH=etag,
    )
    assert resp.status_code == 412
    body = resp.json()
    assert body["etags"]["service.url"] == "v2"
    assert body["current"]["service.url"] == "http://current"


@pytest.mark.django_db
def test_patch_version_mismatch_returns_current_map(client):
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(organization=org, name="Svc", status=Service.Status.ACTIVE, url="http://cur")
    user = User.objects.create_user(username="vol", password="pw", role=User.Role.VOLUNTEER)
    client.force_login(user)

    fv = FieldVersion.objects.create(
        entity_type=FieldVersion.EntityType.SERVICE,
        entity_id=service.id,
        field_path="service.url",
        version=2,
        updated_by=user,
    )
    resp = client.get(reverse("resources:resource-detail", args=[service.id]))
    etag = resp.headers["ETag"]
    data = {
        "service": {"email": "a@b.com"},
        "assert_versions": {"service.url": 1},
    }
    resp = client.patch(
        reverse("resources:resource-detail", args=[service.id]),
        data=json.dumps(data),
        content_type="application/json",
        HTTP_IF_MATCH=etag,
    )
    assert resp.status_code == 409
    body = resp.json()
    assert "service.url" in body["mismatches"]
    assert body["etags"]["service.url"] == "v2"
    assert body["current"]["service.url"] == "http://cur"
