from __future__ import annotations

"""Views providing data health statistics for resources."""

from datetime import timedelta
from typing import Dict

from django.db.models import Exists, OuterRef, Q
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Location, Service
from hsds_ext.models import VerificationEvent
from resources.permissions import IsVolunteer


def get_health_stats() -> Dict[str, int]:
    """Return counts for basic data quality metrics.

    Metrics returned:
        - no_phone: Services without any associated phone numbers.
        - no_hours: Services missing schedule entries.
        - not_geocoded: Locations without latitude or longitude.
        - stale: Services with no verification event in the last 90 days.
    """

    no_phone = Service.objects.filter(phones__isnull=True).count()
    no_hours = Service.objects.filter(schedules__isnull=True).count()
    not_geocoded = Location.objects.filter(Q(latitude__isnull=True) | Q(longitude__isnull=True)).count()

    threshold = timezone.now() - timedelta(days=90)
    recent_verifications = VerificationEvent.objects.filter(
        entity_type=VerificationEvent.EntityType.SERVICE,
        entity_id=OuterRef("pk"),
        verified_at__gte=threshold,
    )
    stale = Service.objects.annotate(has_recent=Exists(recent_verifications)).filter(has_recent=False).count()

    return {
        "no_phone": no_phone,
        "no_hours": no_hours,
        "not_geocoded": not_geocoded,
        "stale": stale,
    }


class HealthStatsView(APIView):
    """Return JSON payload of data health statistics."""

    permission_classes = [IsVolunteer]

    def get(self, request: Request) -> Response:
        stats = get_health_stats()
        data = {
            key: {"count": value} for key, value in stats.items()
        }
        return Response(data)
