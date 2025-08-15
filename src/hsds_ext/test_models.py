"""Tests for HSDS extension models."""
from __future__ import annotations

import uuid

import pytest
from django.db import IntegrityError

from hsds_ext.models.verification import VerificationEvent
from hsds_ext.models.versions import FieldVersion
from hsds_ext.models.sensitive import SensitiveOverlay
from hsds_ext.models.drafts import DraftResource
from hsds_ext.models.change_requests import ChangeRequest
from hsds_ext.models.shelves import Shelf, ShelfMember
from hsds_ext.models.bulk_ops import BulkOperation
from hsds_ext.models.taxonomy_ext import TaxonomyExtension


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


@pytest.mark.django_db
def test_draft_resource_defaults(django_user_model):
    """DraftResource defaults to draft status."""
    user = django_user_model.objects.create_user(username="drafter", password="pw")
    draft = DraftResource.objects.create(created_by=user, payload={"foo": "bar"})
    assert draft.status == DraftResource.Status.DRAFT
    assert draft.payload == {"foo": "bar"}


@pytest.mark.django_db
def test_change_request_status_default(django_user_model):
    """ChangeRequest defaults to pending status."""
    user = django_user_model.objects.create_user(username="submitter", password="pw")
    cr = ChangeRequest.objects.create(
        target_entity_type=ChangeRequest.EntityType.ORGANIZATION,
        target_entity_id=uuid.uuid4(),
        patch=[],
        submitted_by=user,
    )
    assert cr.status == ChangeRequest.Status.PENDING


@pytest.mark.django_db
def test_shelf_member_unique_constraint(django_user_model):
    """Shelf members are unique per shelf/entity."""
    user = django_user_model.objects.create_user(username="owner", password="pw")
    shelf = Shelf.objects.create(owner=user, name="My Shelf")
    ShelfMember.objects.create(
        shelf=shelf,
        entity_type=ShelfMember.EntityType.ORGANIZATION,
        entity_id=uuid.uuid4(),
        added_by=user,
    )
    with pytest.raises(IntegrityError):
        ShelfMember.objects.create(
            shelf=shelf,
            entity_type=ShelfMember.EntityType.ORGANIZATION,
            entity_id=shelf.members.first().entity_id,
            added_by=user,
        )


@pytest.mark.django_db
def test_bulk_operation_default_status(django_user_model):
    """BulkOperation defaults to staged status."""
    user = django_user_model.objects.create_user(username="bulk", password="pw")
    op = BulkOperation.objects.create(
        initiated_by=user,
        scope=BulkOperation.Scope.SHELF,
        targets=[],
        patch=[],
    )
    assert op.status == BulkOperation.Status.STAGED


@pytest.mark.django_db
def test_taxonomy_extension_unique_constraint():
    """TaxonomyExtension unique per entity/namespace/key."""
    eid = uuid.uuid4()
    TaxonomyExtension.objects.create(
        entity_type=TaxonomyExtension.EntityType.ORGANIZATION,
        entity_id=eid,
        namespace="local",
        key="subtype",
        value={"v": 1},
    )
    with pytest.raises(IntegrityError):
        TaxonomyExtension.objects.create(
            entity_type=TaxonomyExtension.EntityType.ORGANIZATION,
            entity_id=eid,
            namespace="local",
            key="subtype",
            value={"v": 2},
        )
