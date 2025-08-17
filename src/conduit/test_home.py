"""Tests for the home page links based on user roles."""
from __future__ import annotations

import pytest
from django.urls import reverse

from users.models import User


@pytest.mark.django_db
def test_volunteer_home_links(client) -> None:
    """Volunteers see only the Pulse link."""
    user = User.objects.create_user(username="vol", password="pass", role=User.Role.VOLUNTEER)
    client.force_login(user)
    resp = client.get(reverse("home"))
    content = resp.content.decode()
    assert "Pulse" in content
    assert "Management" not in content
    assert "Admin" not in content


@pytest.mark.django_db
def test_editor_home_links(client) -> None:
    """Editors see Pulse and Management links."""
    user = User.objects.create_user(username="mgr", password="pass", role=User.Role.EDITOR)
    client.force_login(user)
    resp = client.get(reverse("home"))
    content = resp.content.decode()
    assert "Pulse" in content
    assert "Management" in content
    assert "Admin" not in content


@pytest.mark.django_db
def test_admin_home_links(client) -> None:
    """Admins see links to Pulse, Management, and Admin."""
    user = User.objects.create_user(username="adm", password="pass", role=User.Role.ADMIN)
    client.force_login(user)
    resp = client.get(reverse("home"))
    content = resp.content.decode()
    assert "Pulse" in content
    assert "Management" in content
    assert "Admin" in content
