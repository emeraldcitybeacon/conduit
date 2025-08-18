"""Management command to create default Pulse groups and permissions.

Running this command is safe to execute multiple times.  It ensures that the
required ``Editors`` and ``Volunteers`` groups exist and assigns the relevant
model permissions for the Pulse HSDS extension models.  The command keeps
previously granted permissions intact and simply adds any missing ones.
"""
from __future__ import annotations

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from pulse.permissions import EDITOR_GROUP, VOLUNTEER_GROUP

# Models within the ``hsds_ext`` app that are relevant to Pulse.
PULSE_MODELS = {
    "draftresource",
    "changerequest",
    "mergedraft",
    "duplicateflag",
    "reviewaction",
}

# Volunteers should not receive permissions for audit trails (ReviewAction).
VOLUNTEER_ALLOWED_MODELS = {
    "draftresource",
    "changerequest",
    "mergedraft",
    "duplicateflag",
}


class Command(BaseCommand):
    """Create Pulse role groups with associated permissions."""

    help = "Create or update the default Editors and Volunteers groups."

    def handle(self, *args, **options) -> None:  # pragma: no cover - Django API
        """Entry point for the management command."""

        editor_group, _ = Group.objects.get_or_create(name=EDITOR_GROUP)
        volunteer_group, _ = Group.objects.get_or_create(name=VOLUNTEER_GROUP)

        # Fetch permissions for the Pulse models.
        perms = Permission.objects.filter(
            content_type__app_label="hsds_ext",
            content_type__model__in=PULSE_MODELS,
        )

        # Editors get all permissions on Pulse models.
        editor_group.permissions.add(*perms)

        # Volunteers receive a restricted subset of the permissions.
        volunteer_perms = perms.filter(
            content_type__model__in=VOLUNTEER_ALLOWED_MODELS
        )
        volunteer_group.permissions.add(*volunteer_perms)

        self.stdout.write(self.style.SUCCESS("Pulse roles ensured."))
