"""Conflict badge component used in merge UI."""

from __future__ import annotations

from django_components import register

from ..ui import PulseComponent


@register("conflict_badge")
class ConflictBadge(PulseComponent):
    """Display a small badge indicating a field conflict."""

    template_file = "conflict_badge.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {"label": kwargs.get("label", "conflict")}

