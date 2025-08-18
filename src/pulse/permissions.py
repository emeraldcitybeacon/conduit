"""Utility helpers for Pulse permissions and role checks.

This module defines simple helper functions used throughout the Pulse
application to determine whether a user should have access to editor-only
or volunteer-level features.  These helpers rely on Django's built-in
``Group`` model so that membership can be managed via the admin or a
setup management command.

The module intentionally keeps the checks lightweight – it does not hit the
database for anonymous users and recognises that superusers should always
be treated as editors.
"""
from __future__ import annotations

from django.contrib.auth.models import Group, User

EDITOR_GROUP = "Editors"
VOLUNTEER_GROUP = "Volunteers"


def is_editor(user: User) -> bool:
    """Return ``True`` if the given ``user`` has editor privileges.

    A user qualifies as an editor when they are authenticated and either
    belong to the ``Editors`` group or are marked as a superuser.  The
    check is intentionally simple and does not hit the database for
    anonymous users.
    """

    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=EDITOR_GROUP).exists()


def is_volunteer(user: User) -> bool:
    """Return ``True`` if the given ``user`` has volunteer privileges.

    Volunteers include anyone who is an editor (to avoid repeating checks)
    or who belongs to the ``Volunteers`` group.  Superusers therefore also
    qualify because ``is_editor`` returns ``True`` for them.
    """

    if not user or not user.is_authenticated:
        return False
    if is_editor(user):
        return True
    return user.groups.filter(name=VOLUNTEER_GROUP).exists()


__all__ = ["is_editor", "is_volunteer", "EDITOR_GROUP", "VOLUNTEER_GROUP"]
