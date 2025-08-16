"""UI components for the Pulse app.

This package defines a small base class for Pulse-specific components and
imports concrete component modules so that `django-components` registers them
on import.
"""

from django_components import Component


class PulseComponent(Component):
    """Base component class for all Pulse UI components."""

    # Shared logic or helpers can be added here in the future.
    pass


# Import component modules so that they register with django-components when
# this package is imported.
from . import form_field  # noqa: F401,E402
from . import diff  # noqa: F401,E402
