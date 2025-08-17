"""Views for reviewing drafts within the Pulse UI."""
from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from hsds.models import Service
from hsds_ext.models import ChangeRequest, DraftResource
from resources.serializers.resource import ServiceSerializer
from resources.utils.json_patch import apply_patch
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


@login_required
def change_request_queue(request: HttpRequest) -> HttpResponse:
    """Render pending ChangeRequests for review."""

    if request.user.role not in {User.Role.EDITOR, User.Role.ADMINISTRATOR}:
        return HttpResponseForbidden()
    requests = (
        ChangeRequest.objects.filter(status=ChangeRequest.Status.PENDING)
        .select_related("submitted_by")
        .order_by("-submitted_at")
    )
    return render(request, "pulse/review/queue.html", {"requests": requests})


@login_required
def change_request_detail(request: HttpRequest, id: str) -> HttpResponse:
    """Render a single ``ChangeRequest`` with a field-level diff."""

    if request.user.role not in {User.Role.EDITOR, User.Role.ADMINISTRATOR}:
        return HttpResponseForbidden()
    cr = get_object_or_404(ChangeRequest, id=id)
    service = get_object_or_404(Service, id=cr.target_entity_id)

    original = {"service": ServiceSerializer(service).data}
    patched = apply_patch(original, cr.patch)
    changes = []
    for op in cr.patch:
        field = op.get("path", "").lstrip("/").replace("/", ".")
        before = original
        after = patched
        for part in field.split("."):
            before = before.get(part) if isinstance(before, dict) else None
            after = after.get(part) if isinstance(after, dict) else None
        changes.append({"field": field, "before": before, "after": after})
    context = {"change_request": cr, "changes": changes}
    return render(request, "pulse/review/detail.html", context)
