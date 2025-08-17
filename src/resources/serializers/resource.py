"""Composite serializer for assembling HSDS resources."""
from __future__ import annotations

from typing import Any

from rest_framework import serializers

from hsds.models import Location, Organization, Service
from hsds_ext.models import FieldVersion, SensitiveOverlay
from resources.permissions import AUTO_PUBLISH_FIELDS, REVIEW_REQUIRED_FIELDS
from resources.utils.etags import build_etag_map
from resources.utils.json_paths import delete_value
from users.models import User


class OrganizationSerializer(serializers.ModelSerializer):
    """Minimal representation of an Organization."""

    class Meta:
        model = Organization
        fields = ["id", "name"]


class LocationSerializer(serializers.ModelSerializer):
    """Minimal representation of a Location."""

    class Meta:
        model = Location
        fields = ["id", "name"]


class ServiceSerializer(serializers.ModelSerializer):
    """Editable subset of Service fields."""

    class Meta:
        model = Service
        fields = ["id", "name", "url", "email"]


class ResourceSerializer(serializers.Serializer):
    """Serialize a composite HSDS Resource with version metadata."""

    service = ServiceSerializer()
    organization = OrganizationSerializer()
    location = LocationSerializer(required=False, allow_null=True)
    etags = serializers.DictField(read_only=True)

    def to_representation(self, instance: dict[str, Any]) -> dict[str, Any]:
        """Return composed representation with ETag map and redactions."""

        versions = self.context.get("versions", {})
        overlay: SensitiveOverlay | None = self.context.get("sensitive_overlay")

        data = {
            "service": ServiceSerializer(instance["service"]).data,
            "organization": OrganizationSerializer(instance["organization"]).data,
            "location": (
                LocationSerializer(instance["location"]).data
                if instance.get("location")
                else None
            ),
            "etags": build_etag_map(versions),
        }

        # Apply read-time redaction rules.
        if overlay and overlay.sensitive:
            for path in overlay.visibility_rules.keys():
                delete_value(data, path)
            data["sensitive"] = True
        else:
            data["sensitive"] = False

        return data

    def update(self, instance: dict[str, Any], validated_data: dict[str, Any]) -> dict[str, Any]:
        """Apply validated updates to auto-publish fields and bump versions."""

        service: Service = instance["service"]
        service_data = validated_data.get("service", {})

        user: User = self.context.get("user")
        paths = {f"service.{key}" for key in service_data.keys()}
        if user.role == User.Role.VOLUNTEER:
            forbidden = paths & REVIEW_REQUIRED_FIELDS
            if forbidden:
                raise serializers.ValidationError(
                    {
                        path.split(".", 1)[1]: "review-required"
                        for path in sorted(forbidden)
                    }
                )

        changed_fields: list[str] = []
        if user.role == User.Role.VOLUNTEER:
            allowed_fields = {
                path.split(".", 1)[1]
                for path in AUTO_PUBLISH_FIELDS
                if path.startswith("service.")
            }
            update_items = (
                (field, value)
                for field, value in service_data.items()
                if field in allowed_fields
            )
        else:
            update_items = service_data.items()

        for field, value in update_items:
            setattr(service, field, value)
            changed_fields.append(field)
        if changed_fields:
            service.save(update_fields=changed_fields)
            self._bump_versions(service, changed_fields)
        return instance

    def _bump_versions(self, service: Service, fields: list[str]) -> None:
        """Increment FieldVersion rows for ``service`` ``fields``."""

        user = self.context.get("user")
        for field in fields:
            path = f"service.{field}"
            fv, created = FieldVersion.objects.get_or_create(
                entity_type=FieldVersion.EntityType.SERVICE,
                entity_id=service.id,
                field_path=path,
                defaults={"updated_by": user},
            )
            if not created:
                fv.version += 1
                fv.updated_by = user
                fv.save()
