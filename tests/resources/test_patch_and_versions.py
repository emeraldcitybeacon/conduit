"""Tests for PATCH resource endpoint and FieldVersion behavior."""
from __future__ import annotations

import json

import pytest
from django.urls import reverse

from hsds.models import Organization, Service
from hsds_ext.models import FieldVersion
from users.models import User


@pytest.mark.django_db
def test_patch_updates_versions_and_etag(client):
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org,
        name="Svc",
        status=Service.Status.ACTIVE,
        url="http://old.com",
    )
    user = User.objects.create_user(username="vol", password="pw", role=User.Role.VOLUNTEER)
    client.force_login(user)

    # Seed initial version
    FieldVersion.objects.create(
        entity_type=FieldVersion.EntityType.SERVICE,
        entity_id=service.id,
        field_path="service.url",
        version=1,
        updated_by=user,
    )

    url = reverse("resources:resource-detail", args=[service.id])
    resp = client.get(url)
    etag = resp.headers["ETag"]

    data = {
        "service": {"url": "http://new.com"},
        "assert_versions": {"service.url": 1},
    }
    resp = client.patch(url, data=json.dumps(data), content_type="application/json", HTTP_IF_MATCH=etag)
    assert resp.status_code == 200
    body = resp.json()
    assert body["etags"]["service.url"] == "v2"
    new_etag = resp.headers["ETag"]
    assert new_etag != etag

    fv = FieldVersion.objects.get(field_path="service.url")
    assert fv.version == 2

    # Stale ETag should fail
    data["service"]["url"] = "http://other.com"
    data["assert_versions"]["service.url"] = 2
    resp = client.patch(url, data=json.dumps(data), content_type="application/json", HTTP_IF_MATCH=etag)
    assert resp.status_code == 412

    # Correct ETag but wrong asserted version
    data["assert_versions"]["service.url"] = 1
    resp = client.patch(url, data=json.dumps(data), content_type="application/json", HTTP_IF_MATCH=new_etag)
    assert resp.status_code == 409
