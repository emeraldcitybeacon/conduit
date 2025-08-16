import json
from typing import Any

import pytest
from django.contrib.auth import get_user_model

from hsds.models import Location, Organization, Service

User = get_user_model()


@pytest.fixture
def user_client(client) -> tuple[User, Any]:
    """Return a logged-in volunteer client."""

    user = User.objects.create_user(username="vol", password="pw")
    client.login(username="vol", password="pw")
    return user, client


@pytest.fixture
def services() -> tuple[Service, Service]:
    """Create two services belonging to different orgs."""

    org1 = Organization.objects.create(name="Org1", description="d")
    loc1 = Location.objects.create(location_type="physical", organization=org1, name="Loc1")
    svc1 = Service.objects.create(
        organization=org1,
        name="Svc1",
        description="d",
        status=Service.Status.ACTIVE,
    )
    svc1.locations.add(loc1)

    org2 = Organization.objects.create(name="Org2", description="d")
    loc2 = Location.objects.create(location_type="physical", organization=org2, name="Loc2")
    svc2 = Service.objects.create(
        organization=org2,
        name="Svc2",
        description="d",
        status=Service.Status.ACTIVE,
        url="https://example.org",
    )
    svc2.locations.add(loc2)

    return svc1, svc2


@pytest.mark.django_db
def test_merge_copies_selected_fields_and_deletes_duplicate(user_client, services):
    user, client = user_client
    left, right = services

    payload = {
        "left_id": str(left.id),
        "right_id": str(right.id),
        "fields": ["service.url"],
    }
    response = client.post(
        "/api/merge/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200

    left.refresh_from_db()
    assert left.url == "https://example.org"
    # Duplicate should be removed
    assert not Service.objects.filter(id=right.id).exists()

