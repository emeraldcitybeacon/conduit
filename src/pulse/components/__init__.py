"""Component registry for Pulse app.

This module imports component sub-packages so that ``django-components``
registers them when the ``pulse.components`` package is imported.  Additional
component groups can be added here as the UI grows.
"""

# Import UI and resource component packages for side-effect registration.
from . import resource  # noqa: F401  (Imported for registration)
from . import shelf  # noqa: F401  (Imported for registration)
from . import ui  # noqa: F401  (Imported for registration)
