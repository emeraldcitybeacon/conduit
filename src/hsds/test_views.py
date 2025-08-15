"""Tests for HSDS management views."""
from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from hsds.models import Organization

User = get_user_model()


@pytest.mark.django_db
def test_organization_list_requires_login(client) -> None:
    """Unauthenticated users should be redirected to login."""
    response = client.get(reverse("hsds:organization-list"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_logged_in_user_sees_organization_list(client) -> None:
    """Logged-in users can access the organization list."""
    User.objects.create_user(username="alice", password="secret")
    Organization.objects.create(name="Org", description="Desc")
    client.login(username="alice", password="secret")
    response = client.get(reverse("hsds:organization-list"))
    assert response.status_code == 200
    assert b"Org" in response.content


@pytest.mark.django_db
def test_user_can_create_organization(client) -> None:
    """Posting valid data creates an organization."""
    User.objects.create_user(username="bob", password="secret")
    client.login(username="bob", password="secret")
    response = client.post(
        reverse("hsds:organization-create"),
        {"name": "New Org", "description": "Desc"},
    )
    assert response.status_code == 302
    org = Organization.objects.get(name="New Org")
    assert response.headers["Location"] == reverse(
        "hsds:organization-detail", args=[org.id]
    )


@pytest.mark.django_db
def test_user_can_view_detail(client) -> None:
    """Detail view renders organization information."""
    User.objects.create_user(username="carol", password="secret")
    org = Organization.objects.create(name="Org", description="Desc")
    client.login(username="carol", password="secret")
    response = client.get(reverse("hsds:organization-detail", args=[org.id]))
    assert response.status_code == 200
    assert b"Org" in response.content
