"""Validation hint component for inline form errors."""
from __future__ import annotations

from typing import Iterable

from django_components import Component, register


@register("validator")
class Validator(Component):
    """Render validation error messages for a specific field."""

    template_file = "validator.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        messages = kwargs.get("messages") or []
        if isinstance(messages, str):
            messages = [messages]
        elif isinstance(messages, Iterable):
            messages = list(messages)
        else:
            messages = [str(messages)] if messages else []
        return {
            "field": kwargs.get("field", ""),
            "messages": messages,
        }
