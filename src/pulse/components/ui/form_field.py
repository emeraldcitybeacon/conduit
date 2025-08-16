"""DaisyUI form field wrapper component."""
from __future__ import annotations

from typing import Iterable, List, Tuple

from django_components import register

from . import PulseComponent


@register("form_field")
class FormField(PulseComponent):
    """Render a standard form control with label, help text, and error message.

    Parameters accepted via component kwargs:
        name: ``str`` name attribute for the control.
        label: Optional label displayed above the control.
        field_type: ``"input"`` (default), ``"select"``, or ``"textarea"``.
        input_type: HTML input type when ``field_type`` is ``"input"``.
        value: Pre-filled value for the control.
        options: Iterable of ``(value, label)`` tuples for ``select`` fields.
        help_text: Optional help text shown beneath the control.
        error: Optional validation error text.
    """

    template_file = "form_field.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - simple
        field_type = kwargs.get("field_type", "input")
        options: Iterable[Tuple[str, str]] = kwargs.get("options", []) or []

        # Normalize options into a list of two-tuples.
        normalized: List[Tuple[str, str]] = []
        for option in options:
            if isinstance(option, (list, tuple)) and len(option) == 2:
                normalized.append((str(option[0]), str(option[1])))
            else:
                normalized.append((str(option), str(option)))

        return {
            "name": kwargs.get("name", ""),
            "label": kwargs.get("label", ""),
            "field_type": field_type,
            "input_type": kwargs.get("input_type", "text"),
            "value": kwargs.get("value", ""),
            "options": normalized,
            "help_text": kwargs.get("help_text", ""),
            "error": kwargs.get("error", ""),
        }
