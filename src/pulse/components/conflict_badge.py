"""Conflict badge component used in merge UI."""

from __future__ import annotations

from django_components import Component, register


@register("conflict_badge")
class ConflictBadge(Component):
    """Display a small badge indicating a field conflict."""

    template_file = "conflict_badge.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {"label": kwargs.get("label", "conflict")}
