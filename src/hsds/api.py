"""DRF serializers and viewsets for HSDS models."""

from __future__ import annotations

from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets

from .models import (
    URL,
    Accessibility,
    Address,
    Contact,
    CostOption,
    Funding,
    Language,
    Location,
    Organization,
    OrganizationIdentifier,
    Phone,
    Program,
    RequiredDocument,
    Schedule,
    Service,
    ServiceArea,
    ServiceAtLocation,
    ServiceCapacity,
    Taxonomy,
    TaxonomyTerm,
    Unit,
)


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


class URLSerializer(serializers.ModelSerializer):
    """Serialize :class:`URL` instances."""

    class Meta:
        model = URL
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    """Serialize :class:`Language` instances."""

    class Meta:
        model = Language
        fields = "__all__"


class AccessibilitySerializer(serializers.ModelSerializer):
    """Serialize :class:`Accessibility` instances."""

    class Meta:
        model = Accessibility
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    """Serialize :class:`Address` instances."""

    class Meta:
        model = Address
        fields = "__all__"


class PhoneSerializer(serializers.ModelSerializer):
    """Serialize :class:`Phone` instances with nested languages."""

    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Phone
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    """Serialize :class:`Contact` instances with nested phones."""

    phones = PhoneSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    """Serialize :class:`Schedule` instances."""

    class Meta:
        model = Schedule
        fields = "__all__"


class ServiceAreaSerializer(serializers.ModelSerializer):
    """Serialize :class:`ServiceArea` instances."""

    class Meta:
        model = ServiceArea
        fields = "__all__"


class CostOptionSerializer(serializers.ModelSerializer):
    """Serialize :class:`CostOption` instances."""

    class Meta:
        model = CostOption
        fields = "__all__"


class FundingSerializer(serializers.ModelSerializer):
    """Serialize :class:`Funding` instances."""

    class Meta:
        model = Funding
        fields = "__all__"


class OrganizationIdentifierSerializer(serializers.ModelSerializer):
    """Serialize :class:`OrganizationIdentifier` instances."""

    class Meta:
        model = OrganizationIdentifier
        fields = "__all__"


class RequiredDocumentSerializer(serializers.ModelSerializer):
    """Serialize :class:`RequiredDocument` instances."""

    class Meta:
        model = RequiredDocument
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    """Serialize :class:`Unit` instances."""

    class Meta:
        model = Unit
        fields = "__all__"


class ServiceCapacitySerializer(serializers.ModelSerializer):
    """Serialize :class:`ServiceCapacity` instances with nested unit."""

    unit = UnitSerializer(read_only=True)

    class Meta:
        model = ServiceCapacity
        fields = "__all__"


class TaxonomySerializer(serializers.ModelSerializer):
    """Serialize :class:`Taxonomy` instances."""

    class Meta:
        model = Taxonomy
        fields = "__all__"


class TaxonomyTermSerializer(serializers.ModelSerializer):
    """Serialize :class:`TaxonomyTerm` instances with nested taxonomy."""

    taxonomy_object = TaxonomySerializer(read_only=True)

    class Meta:
        model = TaxonomyTerm
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    """Serialize :class:`Location` instances with related data."""

    addresses = AddressSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    accessibilities = AccessibilitySerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class ServiceAtLocationSerializer(serializers.ModelSerializer):
    """Serialize :class:`ServiceAtLocation` instances with nested relations."""

    location = LocationSerializer(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    service_areas = ServiceAreaSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceAtLocation
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    """Serialize :class:`Service` instances with nested relations."""

    program = ProgramSerializer(read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    service_areas = ServiceAreaSerializer(many=True, read_only=True)
    service_at_locations = ServiceAtLocationSerializer(many=True, read_only=True)
    cost_options = CostOptionSerializer(many=True, read_only=True)
    funding = FundingSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    organization_identifiers = OrganizationIdentifierSerializer(
        many=True, read_only=True
    )
    required_documents = RequiredDocumentSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    capacities = ServiceCapacitySerializer(many=True, read_only=True)
    additional_urls = URLSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = "__all__"

class FilteredModelViewSet(viewsets.ModelViewSet):
    """Base viewset that enables django-filter on all model fields."""

    filterset_fields = "__all__"


class ServiceFilterSet(filters.FilterSet):
    """Filter services by organization, status, or name."""

    class Meta:
        model = Service
        fields = {
            "organization": ["exact"],
            "status": ["exact"],
            "name": ["icontains"],
        }


class OrganizationViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Organization` objects."""

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ProgramViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Program` objects."""

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ServiceViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Service` objects."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_class = ServiceFilterSet


class LocationViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Location` objects."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class AccessibilityViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Accessibility` objects."""

    queryset = Accessibility.objects.all()
    serializer_class = AccessibilitySerializer


class AddressViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Address` objects."""

    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ContactViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Contact` objects."""

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class PhoneViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Phone` objects."""

    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class ScheduleViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Schedule` objects."""

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ServiceAtLocationViewSet(FilteredModelViewSet):
    """API endpoint for :class:`ServiceAtLocation` objects."""

    queryset = ServiceAtLocation.objects.all()
    serializer_class = ServiceAtLocationSerializer


class ServiceAreaViewSet(FilteredModelViewSet):
    """API endpoint for :class:`ServiceArea` objects."""

    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


class CostOptionViewSet(FilteredModelViewSet):
    """API endpoint for :class:`CostOption` objects."""

    queryset = CostOption.objects.all()
    serializer_class = CostOptionSerializer


class FundingViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Funding` objects."""

    queryset = Funding.objects.all()
    serializer_class = FundingSerializer


class LanguageViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Language` objects."""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class OrganizationIdentifierViewSet(FilteredModelViewSet):
    """API endpoint for :class:`OrganizationIdentifier` objects."""

    queryset = OrganizationIdentifier.objects.all()
    serializer_class = OrganizationIdentifierSerializer


class RequiredDocumentViewSet(FilteredModelViewSet):
    """API endpoint for :class:`RequiredDocument` objects."""

    queryset = RequiredDocument.objects.all()
    serializer_class = RequiredDocumentSerializer


class UnitViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Unit` objects."""

    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class ServiceCapacityViewSet(FilteredModelViewSet):
    """API endpoint for :class:`ServiceCapacity` objects."""

    queryset = ServiceCapacity.objects.all()
    serializer_class = ServiceCapacitySerializer


class URLViewSet(FilteredModelViewSet):
    """API endpoint for :class:`URL` objects."""

    queryset = URL.objects.all()
    serializer_class = URLSerializer


class TaxonomyViewSet(FilteredModelViewSet):
    """API endpoint for :class:`Taxonomy` objects."""

    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer


class TaxonomyTermViewSet(FilteredModelViewSet):
    """API endpoint for :class:`TaxonomyTerm` objects."""

    queryset = TaxonomyTerm.objects.all()
    serializer_class = TaxonomyTermSerializer
