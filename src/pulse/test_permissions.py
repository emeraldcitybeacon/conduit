"""Tests for the Pulse permission helpers and role setup command."""
from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, AnonymousUser
from django.core.management import call_command

from pulse.permissions import (
    EDITOR_GROUP,
    VOLUNTEER_GROUP,
    is_editor,
    is_volunteer,
)

User = get_user_model()


@pytest.mark.django_db
class TestPermissionHelpers:
    """Ensure the helper functions behave as expected."""

    def test_is_editor_via_group(self):
        user = User.objects.create(username="ed")
        group = Group.objects.create(name=EDITOR_GROUP)
        user.groups.add(group)
        assert is_editor(user) is True
        assert is_volunteer(user) is True  # Editors qualify as volunteers

    def test_is_volunteer_via_group(self):
        user = User.objects.create(username="vol")
        group = Group.objects.create(name=VOLUNTEER_GROUP)
        user.groups.add(group)
        assert is_editor(user) is False
        assert is_volunteer(user) is True

    def test_anonymous_user(self):
        anon = AnonymousUser()
        assert is_editor(anon) is False
        assert is_volunteer(anon) is False


@pytest.mark.django_db
class TestRoleSetupCommand:
    """Verify that the management command creates groups and permissions."""

    def test_command_creates_groups(self):
        call_command("pulse_setup_roles")
        assert Group.objects.filter(name=EDITOR_GROUP).exists()
        assert Group.objects.filter(name=VOLUNTEER_GROUP).exists()
        editor = Group.objects.get(name=EDITOR_GROUP)
        volunteer = Group.objects.get(name=VOLUNTEER_GROUP)
        # Editors should have at least as many permissions as volunteers
        assert editor.permissions.count() >= volunteer.permissions.count() >= 0
