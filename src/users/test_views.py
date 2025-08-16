"""Tests for authentication views."""
from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_login_page_renders(client) -> None:
    """GET request to the login view should return 200 OK."""
    response = client.get(reverse("users:login"))
    assert response.status_code == 200
    assert b"Sign in" in response.content


@pytest.mark.django_db
def test_user_can_log_in(client) -> None:
    """Posting valid credentials logs the user in and redirects."""
    User.objects.create_user(username="bob", password="secret")
    response = client.post(
        reverse("users:login"),
        {"username": "bob", "password": "secret"},
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


@pytest.mark.django_db
def test_user_can_log_out(client) -> None:
    """Logging out should redirect to the root URL."""
    User.objects.create_user(username="carol", password="secret")
    client.login(username="carol", password="secret")
    response = client.post(reverse("users:logout"))
    assert response.status_code == 302
    assert response.headers["Location"] == "/accounts/login/"
