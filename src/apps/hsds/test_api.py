"""API tests for HSDS core endpoints."""

from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Organization


@pytest.mark.django_db
def test_organization_list_endpoint_returns_created_organization() -> None:
    """Ensure the organization list API returns persisted objects."""

    org = Organization.objects.create(
        name="Test Org",
        description="Desc",
    )

    client = APIClient()
    url = reverse("organization-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data[0]["id"] == str(org.id)

