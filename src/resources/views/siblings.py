"""Endpoints providing sibling service information."""
from __future__ import annotations

from typing import Any, Dict, List

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service
from resources.utils.siblings import get_sibling_data


class SiblingServiceView(APIView):
    """Return services related by organization or location."""

    def get(self, request, id: str) -> Response:
        service = get_object_or_404(
            Service.objects.select_related("organization").prefetch_related("locations"), id=id
        )

        data = get_sibling_data(service)
        return Response(data)
