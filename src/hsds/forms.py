"""Forms for HSDS models."""
from __future__ import annotations

from django import forms

from .models import Organization


class OrganizationForm(forms.ModelForm):
    """Form for creating and updating :class:`~hsds.models.Organization` instances."""

    class Meta:
        model = Organization
        fields = [
            "name",
            "alternate_name",
            "description",
            "email",
            "website",
        ]
