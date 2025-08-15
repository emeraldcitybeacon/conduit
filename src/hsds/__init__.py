"""HSDS app package."""
import sys as _sys

# Ensure the package is importable both as ``hsds`` and ``src.hsds``.
_sys.modules.setdefault("hsds", _sys.modules[__name__])
_sys.modules.setdefault("src.hsds", _sys.modules[__name__])
