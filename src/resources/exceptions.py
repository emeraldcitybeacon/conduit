"""Problem Details exception handler for DRF views."""
from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def problem_detail_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Return RFC7807 problem+json responses for unhandled exceptions."""

    response = exception_handler(exc, context)
    if response is None:
        data = {
            "type": "about:blank",
            "title": "Internal Server Error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": str(exc),
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/problem+json")
    data = {
        "type": "about:blank",
        "title": response.status_text,
        "status": response.status_code,
        "detail": response.data,
    }
    return Response(data, status=response.status_code, content_type="application/problem+json")
