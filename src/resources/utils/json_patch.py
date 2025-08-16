"""Helpers around RFC6902 JSON Patch operations."""

from __future__ import annotations

import copy
from typing import Any, Dict, List

import jsonpatch
from jsonpointer import JsonPointer

JSONPatch = List[Dict[str, Any]]


def apply_patch(document: Any, patch_ops: JSONPatch) -> Any:
    """Apply ``patch_ops`` to ``document`` and return the patched result."""

    patch = jsonpatch.JsonPatch(patch_ops)
    return patch.apply(document, in_place=False)


def diff(source: Any, target: Any) -> JSONPatch:
    """Compute the RFC6902 patch to transform ``source`` into ``target``."""

    return jsonpatch.JsonPatch.from_diff(source, target).patch


def inverse(patch_ops: JSONPatch, source: Any) -> JSONPatch:
    """Return the inverse patch for ``patch_ops`` against ``source``.

    The resulting operations will revert ``patch_ops`` when applied to the
    document produced by ``patch_ops``.
    """

    doc = copy.deepcopy(source)
    inverse_ops: JSONPatch = []
    for op in patch_ops:
        pointer = JsonPointer(op["path"])
        if op["op"] == "add":
            jsonpatch.JsonPatch([op]).apply(doc, in_place=True)
            inverse_ops.insert(0, {"op": "remove", "path": op["path"]})
        elif op["op"] == "remove":
            old = pointer.get(doc)
            jsonpatch.JsonPatch([op]).apply(doc, in_place=True)
            inverse_ops.insert(0, {"op": "add", "path": op["path"], "value": old})
        elif op["op"] == "replace":
            old = pointer.get(doc)
            jsonpatch.JsonPatch([op]).apply(doc, in_place=True)
            inverse_ops.insert(0, {"op": "replace", "path": op["path"], "value": old})
        else:
            raise ValueError(f"Unsupported operation: {op['op']}")
    return inverse_ops
