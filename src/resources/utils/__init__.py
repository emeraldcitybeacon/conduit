"""Utility helpers for Resource facade."""

from .etags import assert_versions, build_etag_map, resource_etag
from .json_patch import apply_patch, diff, inverse
from .json_paths import delete_value, get_value, iter_paths, set_value

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
