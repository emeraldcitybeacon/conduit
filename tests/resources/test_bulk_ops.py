"""Tests for BulkOperation API flow."""
from __future__ import annotations

import json
import uuid

import pytest
from django.urls import reverse

from hsds_ext.models import BulkOperation, Shelf, ShelfMember
from users.models import User


@pytest.mark.django_db
def test_bulk_operation_flow(client):
    user = User.objects.create_user(username="alice", password="pw")
    client.force_login(user)

    shelf = Shelf.objects.create(owner=user, name="Test")
    ShelfMember.objects.create(
        shelf=shelf,
        entity_type="service",
        entity_id=uuid.uuid4(),
        added_by=user,
    )

    patch = [{"op": "replace", "path": "/name", "value": "New"}]
    resp = client.post(
        reverse("resources:bulk-op-stage"),
        {"scope": "shelf", "shelf_id": str(shelf.id), "patch": json.dumps(patch)},
    )
    assert resp.status_code == 201
    op = BulkOperation.objects.get()
    assert op.status == BulkOperation.Status.STAGED

    resp = client.get(reverse("resources:bulk-op-preview", args=[op.id]))
    assert resp.status_code == 200

    resp = client.post(reverse("resources:bulk-op-commit", args=[op.id]))
    assert resp.status_code == 200
    op.refresh_from_db()
    assert op.status == BulkOperation.Status.COMMITTED
    assert op.undo_token

    resp = client.post(
        reverse("resources:bulk-op-undo", args=[op.id]),
        {"undo_token": op.undo_token},
    )
    assert resp.status_code == 200
    op.refresh_from_db()
    assert op.status == BulkOperation.Status.UNDONE
