"""Tests for HSDS management views."""
from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from hsds.models import Organization, Service, Location, Contact

User = get_user_model()


@pytest.mark.django_db
def test_organization_list_requires_login(client) -> None:
    """Unauthenticated users should be redirected to login."""
    response = client.get(reverse("hsds:organization-list"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_logged_in_user_sees_organization_list(client) -> None:
    """Logged-in users can access the organization list."""
    User.objects.create_user(username="alice", password="secret")
    Organization.objects.create(name="Org", description="Desc")
    client.login(username="alice", password="secret")
    response = client.get(reverse("hsds:organization-list"))
    assert response.status_code == 200
    assert b"Org" in response.content


@pytest.mark.django_db
def test_user_can_create_organization(client) -> None:
    """Posting valid data creates an organization."""
    User.objects.create_user(username="bob", password="secret")
    client.login(username="bob", password="secret")
    response = client.post(
        reverse("hsds:organization-create"),
        {"name": "New Org", "description": "Desc"},
    )
    assert response.status_code == 302
    org = Organization.objects.get(name="New Org")
    assert response.headers["Location"] == reverse(
        "hsds:organization-detail", args=[org.id]
    )


@pytest.mark.django_db
def test_user_can_view_detail(client) -> None:
    """Detail view renders organization information."""
    User.objects.create_user(username="carol", password="secret")
    org = Organization.objects.create(name="Org", description="Desc")
    client.login(username="carol", password="secret")
    response = client.get(reverse("hsds:organization-detail", args=[org.id]))
    assert response.status_code == 200
    assert b"Org" in response.content


@pytest.mark.django_db
def test_service_list_requires_login(client) -> None:
    """Unauthenticated users should be redirected to login for service list."""
    response = client.get(reverse("hsds:service-list"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_logged_in_user_sees_service_list(client) -> None:
    """Logged-in users can access the service list."""
    User.objects.create_user(username="dave", password="secret")
    org = Organization.objects.create(name="Org", description="Desc")
    Service.objects.create(organization=org, name="Svc", status="active")
    client.login(username="dave", password="secret")
    response = client.get(reverse("hsds:service-list"))
    assert response.status_code == 200
    assert b"Svc" in response.content


@pytest.mark.django_db
def test_user_can_create_service_with_phone(client) -> None:
    """Posting valid data with phone creates a service."""
    User.objects.create_user(username="erin", password="secret")
    org = Organization.objects.create(name="Org", description="Desc")
    client.login(username="erin", password="secret")
    response = client.post(
        reverse("hsds:service-create"),
        {
            "organization": str(org.id),
            "name": "Svc",
            "status": "active",
            "phones-TOTAL_FORMS": "1",
            "phones-INITIAL_FORMS": "0",
            "phones-MIN_NUM_FORMS": "0",
            "phones-MAX_NUM_FORMS": "1000",
            "phones-0-number": "123",
            "phones-0-type": "voice",
            "schedules-TOTAL_FORMS": "0",
            "schedules-INITIAL_FORMS": "0",
            "schedules-MIN_NUM_FORMS": "0",
            "schedules-MAX_NUM_FORMS": "1000",
        },
    )
    assert response.status_code == 302
    svc = Service.objects.get(name="Svc")
    assert svc.phones.count() == 1


@pytest.mark.django_db
def test_user_can_view_service_detail(client) -> None:
    """Detail view renders service information."""
    User.objects.create_user(username="frank", password="secret")
    org = Organization.objects.create(name="Org", description="Desc")
    svc = Service.objects.create(organization=org, name="Svc", status="active")
    client.login(username="frank", password="secret")
    response = client.get(reverse("hsds:service-detail", args=[svc.id]))
    assert response.status_code == 200
    assert b"Svc" in response.content


@pytest.mark.django_db
def test_location_list_requires_login(client) -> None:
    """Unauthenticated users should be redirected to login for locations."""

    response = client.get(reverse("hsds:location-list"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_logged_in_user_sees_location_list(client) -> None:
    """Logged-in users can access the location list."""

    User.objects.create_user(username="gina", password="secret")
    Location.objects.create(location_type="physical", name="Loc")
    client.login(username="gina", password="secret")
    response = client.get(reverse("hsds:location-list"))
    assert response.status_code == 200
    assert b"Loc" in response.content


@pytest.mark.django_db
def test_user_can_create_location(client) -> None:
    """Posting valid data creates a location."""

    User.objects.create_user(username="henry", password="secret")
    client.login(username="henry", password="secret")
    response = client.post(
        reverse("hsds:location-create"),
        {
            "location_type": "physical",
            "name": "Loc",
            "addresses-TOTAL_FORMS": "0",
            "addresses-INITIAL_FORMS": "0",
            "addresses-MIN_NUM_FORMS": "0",
            "addresses-MAX_NUM_FORMS": "1000",
            "phones-TOTAL_FORMS": "0",
            "phones-INITIAL_FORMS": "0",
            "phones-MIN_NUM_FORMS": "0",
            "phones-MAX_NUM_FORMS": "1000",
            "schedules-TOTAL_FORMS": "0",
            "schedules-INITIAL_FORMS": "0",
            "schedules-MIN_NUM_FORMS": "0",
            "schedules-MAX_NUM_FORMS": "1000",
        },
    )
    assert response.status_code == 302
    loc = Location.objects.get(name="Loc")
    assert response.headers["Location"] == reverse(
        "hsds:location-detail", args=[loc.id]
    )


@pytest.mark.django_db
def test_contact_list_requires_login(client) -> None:
    """Unauthenticated users should be redirected to login for contacts."""

    response = client.get(reverse("hsds:contact-list"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_logged_in_user_sees_contact_list(client) -> None:
    """Logged-in users can access the contact list."""

    User.objects.create_user(username="irene", password="secret")
    Contact.objects.create(name="Alice")
    client.login(username="irene", password="secret")
    response = client.get(reverse("hsds:contact-list"))
    assert response.status_code == 200
    assert b"Alice" in response.content


@pytest.mark.django_db
def test_user_can_create_contact(client) -> None:
    """Posting valid data creates a contact."""

    User.objects.create_user(username="john", password="secret")
    client.login(username="john", password="secret")
    response = client.post(
        reverse("hsds:contact-create"),
        {"name": "Bob"},
    )
    assert response.status_code == 302
    contact = Contact.objects.get(name="Bob")
    assert response.headers["Location"] == reverse(
        "hsds:contact-detail", args=[contact.id]
    )


@pytest.mark.django_db
def test_search_requires_login(client) -> None:
    """Search view should redirect unauthenticated users."""

    response = client.get(reverse("hsds:search"), {"q": "Org"})
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_search_returns_results(client) -> None:
    """Logged-in users receive search results."""

    User.objects.create_user(username="zara", password="secret")
    Organization.objects.create(name="Helpful Org", description="Desc")
    client.login(username="zara", password="secret")
    response = client.get(reverse("hsds:search"), {"q": "Helpful"})
    assert response.status_code == 200
    assert b"Helpful Org" in response.content
