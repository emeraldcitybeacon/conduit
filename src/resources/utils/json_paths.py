"""Utilities for working with dotted JSON paths.

This module provides helpers to access and mutate values inside nested
Python data structures using dotted paths with optional list indices,
for example: ``contacts.phones[0].number``.
"""

from __future__ import annotations

import re
from typing import Any, Iterator, List, Mapping, MutableMapping, MutableSequence, Tuple

Token = Tuple[str, int | None]
_path_re = re.compile(r"([^\.\[]+)(?:\[(\d+)\])?")


def _parse(path: str) -> List[Token]:
    """Parse a dotted path into ``(key, index)`` tokens."""

    tokens: List[Token] = []
    for segment in path.split("."):
        match = _path_re.fullmatch(segment)
        if not match:
            raise ValueError(f"Invalid path segment: {segment!r}")
        key, index = match.groups()
        tokens.append((key, int(index) if index is not None else None))
    return tokens


def get_value(data: Any, path: str, default: Any | None = None) -> Any | None:
    """Return the value at ``path`` inside ``data``.

    ``default`` is returned when any part of the path is missing.
    """

    try:
        obj = data
        for key, idx in _parse(path):
            if not isinstance(obj, Mapping):
                raise KeyError
            obj = obj[key]
            if idx is not None:
                if not isinstance(obj, list):
                    raise KeyError
                obj = obj[idx]
        return obj
    except (KeyError, IndexError, TypeError):
        return default


def set_value(data: MutableMapping[str, Any], path: str, value: Any) -> None:
    """Set ``value`` at ``path`` inside ``data``.

    Intermediate dictionaries or lists are created as needed.
    """

    tokens = _parse(path)
    obj: Any = data
    for i, (key, idx) in enumerate(tokens):
        last = i == len(tokens) - 1
        if last:
            if idx is None:
                obj[key] = value
            else:
                lst = obj.setdefault(key, [])
                if not isinstance(lst, list):
                    raise TypeError(f"Expected list at segment {key!r}")
                while len(lst) <= idx:
                    lst.append(None)
                lst[idx] = value
            return
        # intermediate level
        next_idx = tokens[i + 1][1] if i + 1 < len(tokens) else None
        child = obj.get(key)
        if child is None:
            child = [] if idx is not None else {}
            obj[key] = child
        elif idx is None and not isinstance(child, MutableMapping):
            raise TypeError(f"Expected mapping at segment {key!r}")
        elif idx is not None and not isinstance(child, MutableSequence):
            raise TypeError(f"Expected list at segment {key!r}")
        obj = child
        if idx is not None:
            lst = obj
            while len(lst) <= idx:
                lst.append({} if next_idx is None else [])
            if not isinstance(lst[idx], (MutableMapping, MutableSequence)):
                lst[idx] = {} if next_idx is None else []
            obj = lst[idx]


def delete_value(data: MutableMapping[str, Any], path: str) -> None:
    """Remove the value at ``path`` inside ``data`` if present."""

    tokens = _parse(path)
    obj: Any = data
    for i, (key, idx) in enumerate(tokens):
        last = i == len(tokens) - 1
        if last:
            if idx is None:
                obj.pop(key, None)
            else:
                lst = obj.get(key)
                if isinstance(lst, list) and len(lst) > idx:
                    lst.pop(idx)
            return
        obj = obj.get(key)
        if obj is None:
            return
        if idx is not None:
            if not isinstance(obj, list) or len(obj) <= idx:
                return
            obj = obj[idx]


def iter_paths(data: Any, prefix: str = "") -> Iterator[str]:
    """Yield dotted paths for all leaf nodes within ``data``."""

    if isinstance(data, Mapping):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            yield from iter_paths(value, new_prefix)
    elif isinstance(data, list):
        for idx, value in enumerate(data):
            new_prefix = f"{prefix}[{idx}]" if prefix else f"[{idx}]"
            yield from iter_paths(value, new_prefix)
    else:
        if prefix:
            yield prefix
