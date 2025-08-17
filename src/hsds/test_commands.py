"""Tests for HSDS data export commands."""
from __future__ import annotations

import csv
import json

import pytest
from django.core.management import call_command

from hsds.models import Location, Organization, Service, ServiceAtLocation


@pytest.mark.django_db
def test_export_hsds_json(tmp_path) -> None:
    """Command exports data to JSON file."""

    Organization.objects.create(name="Org", description="Desc")
    output = tmp_path / "export.json"
    call_command("export_hsds_json", str(output))
    data = json.loads(output.read_text())
    assert data["organizations"][0]["name"] == "Org"


@pytest.mark.django_db
def test_export_hsds_csv(tmp_path) -> None:
    """Command exports data to CSV files."""

    Organization.objects.create(name="Org", description="Desc")
    output_dir = tmp_path / "csv"
    call_command("export_hsds_csv", str(output_dir))
    csv_file = output_dir / "organizations.csv"
    assert csv_file.exists()
    rows = list(csv.DictReader(csv_file.open()))
    assert rows[0]["name"] == "Org"


@pytest.mark.django_db
def test_seed_examples_creates_resources() -> None:
    """Command seeds full HSDS resource records."""

    call_command("seed_examples")

    assert Organization.objects.count() == 3
    assert Location.objects.count() == 3
    assert Service.objects.count() == 3
    assert ServiceAtLocation.objects.count() == 3
