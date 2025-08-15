"""Tests for HSDS extension models."""
from __future__ import annotations

import uuid

import pytest
from django.db import IntegrityError

from hsds_ext.models.verification import VerificationEvent
from hsds_ext.models.versions import FieldVersion
from hsds_ext.models.sensitive import SensitiveOverlay


@pytest.mark.django_db
def test_verification_event_creation(django_user_model):
    """Verification events store method and verifier."""
    user = django_user_model.objects.create_user(username="verifier", password="pw")
    event = VerificationEvent.objects.create(
        entity_type=VerificationEvent.EntityType.ORGANIZATION,
        entity_id=uuid.uuid4(),
        field_path="contacts.phones[0].number",
        method=VerificationEvent.Method.CALLED,
        verified_by=user,
    )
    assert event.method == VerificationEvent.Method.CALLED
    assert event.verified_by == user


@pytest.mark.django_db
def test_field_version_unique_constraint(django_user_model):
    """Only one FieldVersion row may exist per entity/field."""
    user = django_user_model.objects.create_user(username="fv", password="pw")
    eid = uuid.uuid4()
    FieldVersion.objects.create(
        entity_type=FieldVersion.EntityType.ORGANIZATION,
        entity_id=eid,
        field_path="name",
        updated_by=user,
    )
    with pytest.raises(IntegrityError):
        FieldVersion.objects.create(
            entity_type=FieldVersion.EntityType.ORGANIZATION,
            entity_id=eid,
            field_path="name",
            updated_by=user,
        )


@pytest.mark.django_db
def test_sensitive_overlay_unique_constraint():
    """SensitiveOverlay is unique per entity."""
    eid = uuid.uuid4()
    SensitiveOverlay.objects.create(
        entity_type=SensitiveOverlay.EntityType.ORGANIZATION,
        entity_id=eid,
    )
    with pytest.raises(IntegrityError):
        SensitiveOverlay.objects.create(
            entity_type=SensitiveOverlay.EntityType.ORGANIZATION,
            entity_id=eid,
        )
