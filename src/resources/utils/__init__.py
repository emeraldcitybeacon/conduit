"""Utility helpers for Resource facade."""

from .json_paths import get_value, set_value, delete_value, iter_paths
from .json_patch import apply_patch, diff, inverse
from .etags import build_etag_map, resource_etag, assert_versions

__all__ = [
    "get_value",
    "set_value",
    "delete_value",
    "iter_paths",
    "apply_patch",
    "diff",
    "inverse",
    "build_etag_map",
    "resource_etag",
    "assert_versions",
]
