"""API endpoints for Worklists (saved searches)."""
from __future__ import annotations

from typing import Any, List

from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
from django.db.models import Q
from django.db.models.functions import Greatest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hsds.models import Service
from hsds_ext.models import Worklist
from resources.permissions import IsVolunteer


def _search_service_ids(query: str) -> List[str]:
    """Return service IDs matching the query using trigram similarity."""

    base_q = Service.objects.filter(name__icontains=query)
    if connection.vendor == "postgresql":
        services = (
            base_q.annotate(
                sim=Greatest(
                    TrigramSimilarity("name", query),
                    TrigramSimilarity("organization__name", query),
                    TrigramSimilarity("phones__number", query),
                    TrigramSimilarity("locations__addresses__address_1", query),
                    TrigramSimilarity("locations__addresses__city", query),
                )
            )
            .order_by("-sim")
            .distinct()[:50]
        )
    else:
        services = base_q.distinct()[:50]
    return [str(s.id) for s in services]


class WorklistListCreateView(APIView):
    """List or create worklists for the current user."""

    permission_classes = [IsVolunteer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request: Request) -> Response:
        worklists = Worklist.objects.filter(owner=request.user).order_by("-created_at")
        data = [
            {"id": str(w.id), "name": w.name, "query": w.query, "is_shared": w.is_shared}
            for w in worklists
        ]
        return Response(data)

    def post(self, request: Request) -> Response:
        name = request.data.get("name")
        query = request.data.get("query")
        if not name or not query:
            return Response(
                {"detail": "Name and query are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        wl = Worklist.objects.create(
            owner=request.user,
            name=name,
            query=query,
            is_shared=bool(request.data.get("is_shared")),
        )
        return Response({"id": str(wl.id), "name": wl.name}, status=status.HTTP_201_CREATED)


class WorklistDetailView(APIView):
    """Retrieve or delete a worklist."""

    permission_classes = [IsVolunteer]

    def get(self, request: Request, id: str) -> Response:
        wl = get_object_or_404(Worklist, id=id, owner=request.user)
        return Response(
            {
                "id": str(wl.id),
                "name": wl.name,
                "query": wl.query,
                "is_shared": wl.is_shared,
            }
        )

    def delete(self, request: Request, id: str) -> Response:
        wl = get_object_or_404(Worklist, id=id, owner=request.user)
        wl.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorklistNavigateView(APIView):
    """Return next or previous service ID in the worklist."""

    permission_classes = [IsVolunteer]

    def get(self, request: Request, id: str, direction: str) -> Response:
        wl = get_object_or_404(Worklist, id=id)
        current = request.query_params.get("current")
        ids = _search_service_ids(wl.query)
        if not ids:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if current and current in ids:
            idx = ids.index(current)
            idx = idx + 1 if direction == "next" else idx - 1
        else:
            idx = 0 if direction == "next" else len(ids) - 1

        if idx < 0 or idx >= len(ids):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({"id": ids[idx]})


class WorklistSearchView(APIView):
    """Return HTML list items for quick-open search results."""

    permission_classes = [IsVolunteer]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        query = request.query_params.get("q", "").strip()
        if not query:
            return HttpResponse("", content_type="text/html")
        ids = _search_service_ids(query)
        services = Service.objects.filter(id__in=ids)
        items = []
        for svc in services:
            label = escape(svc.name or "(no name)")
            items.append(
                f'<li><a href="/pulse/r/{svc.id}/" class="block px-4 py-2 hover:bg-base-200">{label}</a></li>'
            )
        html = "\n".join(items)
        return HttpResponse(html, content_type="text/html")
