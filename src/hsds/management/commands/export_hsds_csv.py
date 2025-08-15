"""Management command to export HSDS data to CSV files."""
from __future__ import annotations

import csv
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
    """Export HSDS data to separate CSV files per model."""

    help = "Export HSDS data to CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "output_dir",
            nargs="?",
            default="hsds_csv",
            help="Directory to write CSV files into",
        )

    def handle(self, *args, **options):
        output_dir = Path(options["output_dir"]).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        mappings = [
            (Organization, OrganizationSerializer),
            (Service, ServiceSerializer),
            (Location, LocationSerializer),
            (Contact, ContactSerializer),
        ]
        for model, serializer_cls in mappings:
            queryset = model.objects.all()
            serializer = serializer_cls(queryset, many=True)
            data = serializer.data
            if not data:
                continue
            file_path = output_dir / f"{model._meta.model_name}s.csv"
            with file_path.open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        self.stdout.write(self.style.SUCCESS(f"Exported CSV files to {output_dir}"))
