"""Views for reviewing drafts within the Pulse UI."""
from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render

from hsds_ext.models import DraftResource
from users.models import User


@login_required
def draft_list(request: HttpRequest) -> HttpResponse:
    """Render a table of drafts awaiting review."""

    if request.user.role not in {User.Role.EDITOR, User.Role.ADMINISTRATOR}:
        return HttpResponseForbidden()
    drafts = (
        DraftResource.objects.filter(status=DraftResource.Status.DRAFT)
        .select_related("created_by")
        .order_by("-created_at")
    )
    return render(request, "pulse/review/drafts_list.html", {"drafts": drafts})
