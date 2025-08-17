"""Tests for ResourceSerializer mapping and version bumping."""
from __future__ import annotations

import pytest
from rest_framework import serializers

from hsds.models import Organization, Service
from hsds_ext.models import FieldVersion, SensitiveOverlay
from resources.serializers.resource import ResourceSerializer
from users.models import User


@pytest.mark.django_db
def test_to_representation_builds_etags_and_applies_overlay():
    """Serializer includes ETag map and redacts via overlay."""
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org,
        name="Svc",
        status=Service.Status.ACTIVE,
        url="http://example.com",
    )
    versions = {"service.url": 3}
    overlay = SensitiveOverlay.objects.create(
        entity_type=SensitiveOverlay.EntityType.SERVICE,
        entity_id=service.id,
        sensitive=True,
        visibility_rules={"service.url": "redact"},
    )
    data = ResourceSerializer(
        instance={"service": service, "organization": org, "location": None},
        context={"versions": versions, "sensitive_overlay": overlay},
    ).data
    assert data["etags"]["service.url"] == "v3"
    assert "url" not in data["service"]
    assert data["sensitive"] is True


@pytest.mark.django_db
def test_update_bumps_field_version():
    """Saving updates the Service and increments FieldVersion."""
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org,
        name="Svc",
        status=Service.Status.ACTIVE,
        url="http://old.com",
    )
    user = User.objects.create_user(username="u", password="pw")
    serializer = ResourceSerializer(
        instance={"service": service, "organization": org, "location": None},
        data={"service": {"url": "http://new.com"}},
        partial=True,
        context={"user": user},
    )
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    service.refresh_from_db()
    assert service.url == "http://new.com"
    fv = FieldVersion.objects.get(
        entity_type=FieldVersion.EntityType.SERVICE,
        entity_id=service.id,
        field_path="service.url",
    )
    assert fv.version == 1
    assert fv.updated_by == user


@pytest.mark.django_db
def test_volunteer_cannot_update_review_required_fields():
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    serializer = ResourceSerializer(
        instance={"service": service, "organization": org},
        data={"service": {"name": "New"}},
        context={"user": user},
        partial=True,
    )
    assert serializer.is_valid()
    with pytest.raises(serializers.ValidationError) as exc:
        serializer.save()
    assert exc.value.detail == {"name": "review-required"}
    service.refresh_from_db()
    assert service.name == "Svc"


@pytest.mark.django_db
def test_volunteer_can_update_auto_publish_fields():
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org,
        name="Svc",
        status=Service.Status.ACTIVE,
        url="http://old.org",
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    serializer = ResourceSerializer(
        instance={"service": service, "organization": org},
        data={"service": {"url": "http://new.org"}},
        context={"user": user},
        partial=True,
    )
    assert serializer.is_valid()
    serializer.save()
    service.refresh_from_db()
    assert service.url == "http://new.org"