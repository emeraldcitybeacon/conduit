"""Render navigation links for sibling services.

This component expects pre-computed sibling lists and navigation metadata to be
passed in by the caller, keeping database access in the view layer.
"""
from __future__ import annotations

from typing import Any, Dict, List

from django_components import Component, register


@register("siblings_nav")
class SiblingsNav(Component):
    """Render sibling navigation lists for a service."""

    template_file = "siblings_nav.html"

    def get_template_data(
        self, args: List[Any], kwargs: Dict[str, Any], slots, context: Dict[str, Any]
    ) -> Dict[str, Any]:  # pragma: no cover - simple mapping
        """Forward provided kwargs to template variables."""

        return {
            "loc_siblings": kwargs.get("loc_siblings", []),
            "org_siblings": kwargs.get("org_siblings", []),
            "prev_id": kwargs.get("prev_id", ""),
            "next_id": kwargs.get("next_id", ""),
            "first_loc": kwargs.get("first_loc", ""),
            "first_org": kwargs.get("first_org", ""),
        }
