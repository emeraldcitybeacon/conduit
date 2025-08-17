"""Management command to seed example HSDS resources."""
from __future__ import annotations

from django.core.management.base import BaseCommand

from hsds.models import (
    Address,
    Location,
    Organization,
    Phone,
    Service,
    ServiceAtLocation,
)

EXAMPLES = [
    {
        "organization": {
            "name": "Helping Hands",
            "description": "Provides community support services",
        },
        "location": {
            "name": "Helping Hands Center",
            "location_type": Location.LocationType.PHYSICAL,
            "description": "Main service center",
            "address": {
                "address_1": "123 Main St",
                "city": "Metropolis",
                "state_province": "CA",
                "postal_code": "90210",
                "country": "US",
                "address_type": Address.AddressType.PHYSICAL,
            },
            "phone": {
                "number": "555-0100",
                "type": Phone.PhoneType.VOICE,
            },
        },
        "service": {
            "name": "Food Pantry",
            "status": Service.Status.ACTIVE,
            "description": "Free weekly groceries for low-income residents",
        },
    },
    {
        "organization": {
            "name": "Wellness Works",
            "description": "Community health organization",
        },
        "location": {
            "name": "Wellness Works Clinic",
            "location_type": Location.LocationType.PHYSICAL,
            "description": "Walk-in health services",
            "address": {
                "address_1": "456 Elm St",
                "city": "Springfield",
                "state_province": "IL",
                "postal_code": "62704",
                "country": "US",
                "address_type": Address.AddressType.PHYSICAL,
            },
            "phone": {
                "number": "555-0101",
                "type": Phone.PhoneType.VOICE,
            },
        },
        "service": {
            "name": "Community Clinic",
            "status": Service.Status.ACTIVE,
            "description": "Basic medical care for all ages",
        },
    },
    {
        "organization": {
            "name": "Job Futures",
            "description": "Employment and training assistance",
        },
        "location": {
            "name": "Job Futures Office",
            "location_type": Location.LocationType.PHYSICAL,
            "description": "Career counseling center",
            "address": {
                "address_1": "789 Oak Ave",
                "city": "Gotham",
                "state_province": "NY",
                "postal_code": "10001",
                "country": "US",
                "address_type": Address.AddressType.PHYSICAL,
            },
            "phone": {
                "number": "555-0102",
                "type": Phone.PhoneType.VOICE,
            },
        },
        "service": {
            "name": "Job Training Program",
            "status": Service.Status.ACTIVE,
            "description": "Workforce readiness workshops",
        },
    },
]


class Command(BaseCommand):
    """Seed the database with example HSDS resources."""

    help = "Create example organizations, locations, and services"

    def handle(self, *args, **options):
        for example in EXAMPLES:
            org_data = example["organization"]
            org, _ = Organization.objects.get_or_create(
                name=org_data["name"], defaults=org_data
            )

            loc_data = example["location"]
            location, _ = Location.objects.get_or_create(
                organization=org,
                name=loc_data["name"],
                defaults={
                    "location_type": loc_data.get(
                        "location_type", Location.LocationType.PHYSICAL
                    ),
                    "description": loc_data.get("description", ""),
                },
            )
            addr = loc_data.get("address")
            if addr:
                Address.objects.get_or_create(location=location, **addr)
            phone_data = loc_data.get("phone")
            if phone_data:
                Phone.objects.get_or_create(
                    location=location,
                    organization=org,
                    number=phone_data["number"],
                    defaults=phone_data,
                )

            svc_data = example["service"]
            service, _ = Service.objects.get_or_create(
                organization=org,
                name=svc_data["name"],
                defaults={
                    "status": svc_data.get("status", Service.Status.ACTIVE),
                    "description": svc_data.get("description", ""),
                },
            )

            ServiceAtLocation.objects.get_or_create(service=service, location=location)

        self.stdout.write(self.style.SUCCESS("Seeded example resources"))
