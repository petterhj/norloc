from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from locations.models import (
    Location,
    Photo,
    NameType,
    Municipality,
    NO_COUNTIES,
)
from locations.serializers import (
    LocationSerializer,
    LocationListSerializer,
    NameTypeSerializer,
    PhotoSerializer,
)


class NameTypeViewSet(viewsets.ModelViewSet):
    queryset = NameType.objects.all().order_by('name')
    serializer_class = NameTypeSerializer
    lookup_field = 'slug'


class CountiesViewSet(viewsets.ViewSet):
    def list(self, *args, **kwargs):
        municipalities = Municipality.objects.order_by('county').distinct('county')
        all_counties = {slug: name for slug, name in NO_COUNTIES}
        
        return Response([{
            "slug": municipality.county,
            "name": all_counties[municipality.county],
         } for municipality in municipalities])


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('name')
    serializer_class = LocationSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create']:
            return LocationSerializer
        else: 
            return LocationListSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        filters = {}

        if 'type' in self.kwargs:
            filters['name_types__slug'] = self.kwargs['type']
        if 'county' in self.kwargs:
            filters['municipality__county'] = self.kwargs['county']
        if 'municipality' in self.kwargs:
            filters['municipality__slug'] = self.kwargs['municipality']

        return queryset.filter(**filters)


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(
            location__slug=self.kwargs['slug']
        )  
