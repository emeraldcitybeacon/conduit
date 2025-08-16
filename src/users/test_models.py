"""Tests for the custom User model."""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user_with_role() -> None:
    """Creating a user should persist the specified role."""
    user = User.objects.create_user(
        username="alice",
        password="password123",
        role=User.Role.EDITOR,
    )
    assert user.role == User.Role.EDITOR


def test_role_choices() -> None:
    """Role choices should include administrator, editor, and volunteer."""
    assert set(User.Role.values) == {"administrator", "editor", "volunteer"}


@pytest.mark.django_db
def test_default_role_is_volunteer() -> None:
    """Users without an explicit role default to ``volunteer``."""

    user = User.objects.create_user(username="eve", password="password123")
    assert user.role == User.Role.VOLUNTEER

