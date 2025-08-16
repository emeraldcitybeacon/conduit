"""Tests for bulk operation API endpoints."""
from __future__ import annotations

import json
import uuid

import pytest
from django.contrib.auth import get_user_model

from hsds_ext.models import BulkOperation, Shelf, ShelfMember

User = get_user_model()


@pytest.mark.django_db
def test_bulk_operation_flow(client) -> None:
    """User can stage, commit, and undo a bulk operation."""

    user = User.objects.create_user(username="alice", password="pw")
    client.force_login(user)

    shelf = Shelf.objects.create(owner=user, name="Test Shelf")
    ShelfMember.objects.create(
        shelf=shelf,
        entity_type="service",
        entity_id=uuid.uuid4(),
        added_by=user,
    )

    patch = [{"op": "replace", "path": "/name", "value": "New"}]
    resp = client.post(
        "/api/bulk-ops/",
        {
            "scope": "shelf",
            "shelf_id": str(shelf.id),
            "patch": json.dumps(patch),
        },
    )
    assert resp.status_code == 201

    op = BulkOperation.objects.get()
    assert len(op.targets) == 1
    assert op.status == BulkOperation.Status.STAGED

    resp = client.get(f"/api/bulk-ops/{op.id}/preview/")
    assert resp.status_code == 200

    resp = client.post(f"/api/bulk-ops/{op.id}/commit/")
    assert resp.status_code == 200
    op.refresh_from_db()
    assert op.status == BulkOperation.Status.COMMITTED
    assert op.undo_token

    resp = client.post(
        f"/api/bulk-ops/{op.id}/undo/",
        {"undo_token": op.undo_token},
    )
    assert resp.status_code == 200
    op.refresh_from_db()
    assert op.status == BulkOperation.Status.UNDONE
