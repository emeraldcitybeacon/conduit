"""Views for the multi-step resource creation wizard."""
from __future__ import annotations

import json
from typing import Dict

from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from hsds_ext.models import DraftResource


class WizardStartView(TemplateView):
    """Landing page for the creation wizard."""

    template_name = "pulse/wizard/start.html"

    def get(self, request, *args, **kwargs):  # pragma: no cover - trivial
        request.session.pop("wizard", None)
        return super().get(request, *args, **kwargs)


class OrgStepView(View):
    """Collect organization information."""

    template_name = "pulse/wizard/step_org.html"

    def get(self, request):  # pragma: no cover - simple render
        return render(request, self.template_name)

    def post(self, request):
        request.session.setdefault("wizard", {})["organization"] = {
            "name": request.POST.get("name", ""),
        }
        request.session.modified = True
        return redirect("pulse:wizard-location")


class LocationStepView(View):
    """Collect location information."""

    template_name = "pulse/wizard/step_location.html"

    def get(self, request):  # pragma: no cover - simple render
        return render(request, self.template_name)

    def post(self, request):
        request.session.setdefault("wizard", {})["location"] = {
            "name": request.POST.get("name", ""),
            "address": request.POST.get("address", ""),
        }
        request.session.modified = True
        return redirect("pulse:wizard-service")


class ServiceStepView(View):
    """Collect service info and create the draft resource."""

    template_name = "pulse/wizard/step_service.html"

    def get(self, request):  # pragma: no cover - simple render
        return render(request, self.template_name)

    def post(self, request):
        wizard: Dict[str, Dict[str, str]] = request.session.setdefault("wizard", {})
        if "confirm" in request.POST:
            payload = {
                "organization": wizard.get("organization", {}),
                "location": wizard.get("location", {}),
                "service": wizard.get("service", {}),
            }
            DraftResource.objects.create(
                created_by=request.user,
                payload=payload,
            )
            request.session.pop("wizard", None)
            return redirect("pulse:dashboard")

        wizard["service"] = {"name": request.POST.get("name", "")}
        request.session.modified = True
        payload = {
            "organization": wizard.get("organization", {}),
            "location": wizard.get("location", {}),
            "service": wizard.get("service", {}),
        }
        json_payload = json.dumps(payload, indent=2)
        return render(
            request,
            self.template_name,
            {"preview": True, "payload": json_payload},
        )
