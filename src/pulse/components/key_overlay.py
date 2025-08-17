"""Modal overlay listing keyboard shortcuts from a JSON registry."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

from django.conf import settings
from django_components import Component, register

REGISTRY_PATH = (
    Path(settings.BASE_DIR).parent / "pulse" / "static" / "pulse" / "keys.json"
)


@lru_cache
def _load_registry() -> Dict[str, List[Dict[str, Any]]]:
    """Load and cache the keyboard shortcuts registry from disk."""
    with REGISTRY_PATH.open() as fh:
        return json.load(fh)


@register("key_overlay")
class KeyOverlay(Component):
    """Render a modal dialog showing keyboard shortcuts.

    Parameters
    ----------
    scope:
        Optional scope name to include bindings for. Bindings under the
        "global" scope are always included.
    id:
        HTML id for the dialog element. Defaults to ``key-overlay``.
    """

    template_file = "key_overlay.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        scope = kwargs.get("scope", "global")
        registry = _load_registry()
        bindings: List[Dict[str, Any]] = list(registry.get("global", []))
        if scope != "global":
            bindings.extend(registry.get(scope, []))
        return {
            "id": kwargs.get("id", "key-overlay"),
            "bindings": bindings,
        }
