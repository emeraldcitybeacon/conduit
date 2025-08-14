"""DRF serializers and viewsets for HSDS core models."""

from __future__ import annotations

from rest_framework import serializers, viewsets

from .models import Location, Organization, Program, Service


class OrganizationSerializer(serializers.ModelSerializer):
    """Serialize :class:`Organization` instances."""

    class Meta:
        model = Organization
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    """Serialize :class:`Program` instances."""

    class Meta:
        model = Program
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    """Serialize :class:`Service` instances."""

    class Meta:
        model = Service
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    """Serialize :class:`Location` instances."""

    class Meta:
        model = Location
        fields = "__all__"


class OrganizationViewSet(viewsets.ModelViewSet):
    """API endpoint for :class:`Organization` objects."""

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    """API endpoint for :class:`Program` objects."""

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """API endpoint for :class:`Service` objects."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """API endpoint for :class:`Location` objects."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

