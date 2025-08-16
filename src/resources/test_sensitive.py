"""Tests for sensitive overlay endpoints and redaction."""
from __future__ import annotations

import pytest
from django.urls import reverse

from hsds.models import Organization, Service
from hsds_ext.models import SensitiveOverlay
from users.models import User


@pytest.mark.django_db
def test_patch_sensitive_overlay_sets_rules(client, django_user_model):
    """PATCH endpoint creates or updates the overlay with given rules."""

    editor = django_user_model.objects.create_user(
        username="editor", password="pw", role=User.Role.EDITOR
    )
    client.force_login(editor)

    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )

    url = reverse("resources:resource-sensitive", args=[service.id])
    resp = client.patch(
        url,
        {"sensitive": True, "visibility_rules": {"service.url": "redact"}},
        content_type="application/json",
    )

    assert resp.status_code == 200
    overlay = SensitiveOverlay.objects.get(
        entity_type=SensitiveOverlay.EntityType.SERVICE, entity_id=service.id
    )
    assert overlay.sensitive is True
    assert overlay.visibility_rules == {"service.url": "redact"}


@pytest.mark.django_db
def test_resource_serialization_redacts_with_overlay(client, django_user_model):
    """Serializer output omits paths defined in visibility rules."""

    user = django_user_model.objects.create_user(username="vol", password="pw")
    client.force_login(user)

    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org,
        name="Svc",
        status=Service.Status.ACTIVE,
        url="http://example.com",
    )

    SensitiveOverlay.objects.create(
        entity_type=SensitiveOverlay.EntityType.SERVICE,
        entity_id=service.id,
        sensitive=True,
        visibility_rules={"service.url": "redact"},
    )

    url = reverse("resources:resource-detail", args=[service.id])
    resp = client.get(url)

    assert resp.status_code == 200
    data = resp.json()
    assert "url" not in data["service"]
    assert data["sensitive"] is True

