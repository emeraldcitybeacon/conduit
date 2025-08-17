import pytest
from rest_framework import serializers

from hsds.models import Organization, Service
from resources.serializers.resource import ResourceSerializer
from users.models import User


@pytest.mark.django_db
def test_volunteer_cannot_update_review_required_fields():
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    serializer = ResourceSerializer(
        instance={"service": service, "organization": org},
        data={"service": {"name": "New"}},
        context={"user": user},
        partial=True,
    )
    assert serializer.is_valid()
    with pytest.raises(serializers.ValidationError) as exc:
        serializer.save()
    assert exc.value.detail == {"name": "review-required"}
    service.refresh_from_db()
    assert service.name == "Svc"


@pytest.mark.django_db
def test_volunteer_can_update_auto_publish_fields():
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org,
        name="Svc",
        status=Service.Status.ACTIVE,
        url="http://old.org",
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    serializer = ResourceSerializer(
        instance={"service": service, "organization": org},
        data={"service": {"url": "http://new.org"}},
        context={"user": user},
        partial=True,
    )
    assert serializer.is_valid()
    serializer.save()
    service.refresh_from_db()
    assert service.url == "http://new.org"
