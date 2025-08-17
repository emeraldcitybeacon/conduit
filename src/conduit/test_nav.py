"""Tests for the navigation component based on user roles."""
from __future__ import annotations

import pytest
from django.urls import reverse

from users.models import User


@pytest.mark.django_db
def test_volunteer_nav(client) -> None:
    """Volunteers see Pulse dropdown but not Admin link."""

    user = User.objects.create_user(username="vol", password="pass", role=User.Role.VOLUNTEER)
    client.force_login(user)
    resp = client.get(reverse("hsds:dashboard"))
    content = resp.content.decode()
    assert "Pulse" in content
    assert "Worklists" in content
    assert "Admin" not in content


@pytest.mark.django_db
def test_manager_nav(client) -> None:
    """Editors see Pulse and Management menus but not Admin link."""

    user = User.objects.create_user(username="mgr", password="pass", role=User.Role.EDITOR)
    client.force_login(user)
    resp = client.get(reverse("hsds:dashboard"))
    content = resp.content.decode()
    assert "Pulse" in content
    assert "Review queue" in content
    assert "Admin" not in content


@pytest.mark.django_db
def test_admin_nav(client) -> None:
    """Admins see Pulse and Management menus plus Admin link."""

    user = User.objects.create_user(username="adm", password="pass", role=User.Role.ADMIN)
    client.force_login(user)
    resp = client.get(reverse("hsds:dashboard"))
    content = resp.content.decode()
    assert "Pulse" in content
    assert "Review queue" in content
    assert "Admin" in content
