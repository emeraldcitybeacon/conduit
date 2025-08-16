"""Field verification action button."""
from __future__ import annotations

from django_components import register

from ..ui import PulseComponent


@register("verify_button")
class VerifyButton(PulseComponent):
    """Render a button used to record a verification event.

    Parameters via component kwargs:
        label: Button text.
        method: Verification method identifier.
        field_path: Dot-path identifying the field being verified.
        resource_id: UUID of the resource/service.
    """

    template_file = "verify_button.html"

    def get_template_data(self, args, kwargs, slots, context):  # pragma: no cover - trivial
        return {
            "label": kwargs.get("label", "Verify"),
            "method": kwargs.get("method", "called"),
            "field_path": kwargs.get("field_path", ""),
            "resource_id": kwargs.get("resource_id"),
        }
