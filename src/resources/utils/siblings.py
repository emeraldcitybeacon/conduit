from __future__ import annotations

"""Utility helpers for computing sibling service lists and navigation data."""

from typing import Any, Dict, List

from hsds.models import Service


def get_sibling_data(service: Service) -> Dict[str, Any]:
    """Return sibling services grouped by organization and location.

    Args:
        service: Reference service instance.

    Returns:
        dict: Contains ``organization`` and ``location`` lists of sibling
        services. Each list entry is a dict with ``id`` and ``name``. The
        payload also includes navigation helpers ``prev_id``, ``next_id``,
        ``first_org`` and ``first_loc`` for keyboard shortcuts.
    """

    org_qs = (
        Service.objects.filter(organization=service.organization)
        .exclude(id=service.id)
        .order_by("name")
    )
    org = [{"id": str(s.id), "name": s.name} for s in org_qs]

    loc: List[Dict[str, Any]] = []
    prev_id = next_id = first_loc = ""
    location = service.locations.first()
    if location:
        loc_all = list(location.services.order_by("name"))
        loc = [
            {"id": str(s.id), "name": s.name}
            for s in loc_all
            if s.id != service.id
        ]
        ids = [str(s.id) for s in loc_all]
        try:
            idx = ids.index(str(service.id))
            if idx > 0:
                prev_id = ids[idx - 1]
            if idx + 1 < len(ids):
                next_id = ids[idx + 1]
        except ValueError:
            pass
        if loc:
            first_loc = loc[0]["id"]

    first_org = org[0]["id"] if org else ""

    return {
        "organization": org,
        "location": loc,
        "prev_id": prev_id,
        "next_id": next_id,
        "first_loc": first_loc,
        "first_org": first_org,
    }
