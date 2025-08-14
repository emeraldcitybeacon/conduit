"""Tests for HSDS management views."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Organization


@pytest.mark.django_db
def test_organization_list_view_loads(client) -> None:
    """Logged in users can access the organization list."""
    user = get_user_model().objects.create_user(
        username="tester", password="pass"
    )
    client.force_login(user)
    response = client.get(reverse("hsds:organization_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_organization_create_view_creates_org(client) -> None:
    """Posting valid data creates an organization and redirects via HTMX."""
    user = get_user_model().objects.create_user(
        username="creator", password="pass"
    )
    client.force_login(user)
    url = reverse("hsds:organization_create")
    response = client.post(
        url,
        {"name": "Org", "description": "Desc"},
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 204
    org = Organization.objects.get(name="Org")
    assert response.headers["HX-Redirect"] == reverse(
        "hsds:organization_detail", args=[org.pk]
    )
