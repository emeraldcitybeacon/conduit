"""Weak ETag helpers based on field-version maps."""

from __future__ import annotations

import hashlib
import json
from typing import Mapping, Dict, Any


def build_etag_map(versions: Mapping[str, int]) -> Dict[str, str]:
    """Convert raw version integers to ``v<version>`` strings."""

    return {path: f"v{version}" for path, version in versions.items()}


def resource_etag(versions: Mapping[str, int]) -> str:
    """Compute a weak ETag for an entire resource.

    The ETag is derived from the JSON representation of ``versions`` and thus
    changes whenever any field version changes.
    """

    payload = json.dumps(versions, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return f'W/"{digest}"'


def assert_versions(current: Mapping[str, int], asserted: Mapping[str, int]) -> list[str]:
    """Return a list of field paths whose versions do not match ``current``."""

    mismatches: list[str] = []
    for path, version in asserted.items():
        if current.get(path) != version:
            mismatches.append(path)
    return mismatches
