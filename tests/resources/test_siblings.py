import pytest
import pytest
from django.urls import reverse

from hsds.models import Organization, Service, Location, ServiceAtLocation


@pytest.mark.django_db
def test_sibling_service_view(client):
    org = Organization.objects.create(name="Org", description="d")
    service1 = Service.objects.create(
        organization=org, name="A", status=Service.Status.ACTIVE
    )
    service2 = Service.objects.create(
        organization=org, name="B", status=Service.Status.ACTIVE
    )
    loc = Location.objects.create(
        location_type=Location.LocationType.PHYSICAL,
        organization=org,
        name="Loc",
    )
    ServiceAtLocation.objects.create(service=service1, location=loc)
    ServiceAtLocation.objects.create(service=service2, location=loc)

    url = reverse("resources:resource-siblings", args=[service1.id])
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert any(s["id"] == str(service2.id) for s in data["organization"])
    assert any(s["id"] == str(service2.id) for s in data["location"])
