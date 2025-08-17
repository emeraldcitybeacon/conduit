"""Render navigation links to sibling services.

This component expects pre-fetched sibling data and simply renders
navigation links. Data fetching lives in views to keep components thin.
"""
from __future__ import annotations

from typing import Any, Dict

from django_components import Component, register


@register("siblings_nav")
class SiblingsNav(Component):
    """Render sibling navigation lists for a service.

    Keyword Args:
        data (dict): Mapping containing ``loc_siblings`` and
            ``org_siblings`` lists along with optional navigation
            metadata (``prev_id``, ``next_id``, ``first_loc``,
            ``first_org``).
    """

    template_file = "siblings_nav.html"

    def get_template_data(self, args, kwargs, slots, context) -> Dict[str, Any]:  # pragma: no cover - simple pass-through
        """Return the provided sibling data for template rendering."""

        return kwargs.get("data", {})
