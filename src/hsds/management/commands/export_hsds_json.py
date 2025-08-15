"""Management command to export HSDS data to JSON."""
from __future__ import annotations

import json
from pathlib import Path

from django.core.management.base import BaseCommand

from hsds.api import (
    ContactSerializer,
    LocationSerializer,
    OrganizationSerializer,
    ServiceSerializer,
)
from hsds.models import Contact, Location, Organization, Service


class Command(BaseCommand):
    """Export HSDS data to a single JSON file."""

    help = "Export HSDS data to a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "output",
            nargs="?",
            default="hsds_export.json",
            help="Path to the output JSON file",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"]).expanduser().resolve()
        data = {
            "organizations": OrganizationSerializer(Organization.objects.all(), many=True).data,
            "services": ServiceSerializer(Service.objects.all(), many=True).data,
            "locations": LocationSerializer(Location.objects.all(), many=True).data,
            "contacts": ContactSerializer(Contact.objects.all(), many=True).data,
        }
        with output_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        self.stdout.write(self.style.SUCCESS(f"Exported data to {output_path}"))
