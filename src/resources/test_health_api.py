import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from hsds.models import Location, Organization, Service, ServiceAtLocation

User = get_user_model()


@pytest.mark.django_db
def test_health_stats_endpoint(client) -> None:
    """Health stats endpoint returns expected counts."""

    user = User.objects.create_user(username="vol", password="pw")
    client.login(username="vol", password="pw")

    org = Organization.objects.create(name="Org", description="d")
    loc = Location.objects.create(location_type="physical", organization=org, name="Loc")
    svc = Service.objects.create(organization=org, name="Svc", status="active")
    ServiceAtLocation.objects.create(service=svc, location=loc)

    url = reverse("resources:health-stats")
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data["no_phone"]["count"] == 1
    assert data["no_hours"]["count"] == 1
    assert data["not_geocoded"]["count"] == 1
    assert data["stale"]["count"] == 1
