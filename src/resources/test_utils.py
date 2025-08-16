"""Tests for resource utility helpers."""
from __future__ import annotations

from resources.utils import (
    apply_patch,
    assert_versions,
    build_etag_map,
    delete_value,
    diff,
    get_value,
    inverse,
    iter_paths,
    resource_etag,
    set_value,
)


def test_json_path_helpers():
    """Values can be accessed, mutated, and removed via dotted paths."""

    doc = {"contacts": {"phones": [{"number": "123"}]}}
    assert get_value(doc, "contacts.phones[0].number") == "123"

    set_value(doc, "contacts.phones[0].number", "456")
    assert doc["contacts"]["phones"][0]["number"] == "456"

    delete_value(doc, "contacts.phones[0].number")
    assert get_value(doc, "contacts.phones[0].number") is None

    assert set(iter_paths(doc)) == set()


def test_json_patch_diff_and_inverse():
    """Diff and inverse operations round-trip a document."""

    source = {"a": 1, "b": {"c": 2}}
    target = {"a": 1, "b": {"c": 3, "d": 4}}
    patch_ops = diff(source, target)
    patched = apply_patch(source, patch_ops)
    assert patched == target

    undo = inverse(patch_ops, source)
    restored = apply_patch(patched, undo)
    assert restored == source


def test_etag_helpers_change_when_versions_change():
    """ETags reflect field version changes and mismatches are detected."""

    versions = {"name": 1, "contacts.phones[0].number": 2}
    etag_map = build_etag_map(versions)
    assert etag_map["name"] == "v1"

    etag1 = resource_etag(versions)
    versions["name"] = 3
    etag2 = resource_etag(versions)
    assert etag1 != etag2

    mismatches = assert_versions(versions, {"name": 2})
    assert mismatches == ["name"]
