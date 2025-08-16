"""Toast card component for duplicate hints."""
from __future__ import annotations

from typing import Any, Dict

from django_components import register

from . import PulseComponent


@register("toast_card")
class ToastCard(PulseComponent):
    """Render a daisyUI card suitable for use inside a toast container.

    Parameters passed to the component via the template tag:
        ``title``:   Heading text for the card.
        ``body``:    Supporting text displayed beneath the title.
        ``href``:    Optional URL for a call-to-action button.
    """

    template_file = "toast_card.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Return context variables for rendering the card."""

        return {
            "title": kwargs.get("title", ""),
            "body": kwargs.get("body", ""),
            "href": kwargs.get("href"),
        }
