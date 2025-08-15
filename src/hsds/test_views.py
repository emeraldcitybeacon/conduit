"""Tests for HSDS management views."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest

from .models import Organization

User = get_user_model()


@pytest.mark.django_db
def test_organization_list_requires_login(client) -> None:
    """Unauthenticated users should be redirected to the login page."""
    response = client.get(reverse("hsds:organization-list"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_organization_list_renders_for_authenticated_user(client) -> None:
    """Authenticated users should see the list of organizations."""
    user = User.objects.create_user(username="user", password="pass")
    Organization.objects.create(name="Org1", description="Desc")
    client.login(username="user", password="pass")
    response = client.get(reverse("hsds:organization-list"))
    assert response.status_code == 200
    assert b"Org1" in response.content


@pytest.mark.django_db
def test_organization_create_via_htmx(client) -> None:
    """Posting valid data should create an organization and return HX-Redirect."""
    user = User.objects.create_user(username="alice", password="secret")
    client.login(username="alice", password="secret")
    response = client.post(
        reverse("hsds:organization-create"),
        {"name": "Test Org", "description": "Desc"},
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert response.headers["HX-Redirect"].endswith("/manage/organizations/" + str(Organization.objects.first().pk) + "/")
    assert Organization.objects.filter(name="Test Org").exists()


@pytest.mark.django_db
def test_organization_detail_view(client) -> None:
    """Detail view should render organization information."""
    user = User.objects.create_user(username="bob", password="secret")
    org = Organization.objects.create(name="Org2", description="Desc")
    client.login(username="bob", password="secret")
    response = client.get(reverse("hsds:organization-detail", args=[org.pk]))
    assert response.status_code == 200
    assert b"Org2" in response.content
