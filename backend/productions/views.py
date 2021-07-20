from django.http import Http404
from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from productions.models import (
    Production,
    Scene,
    Research,
    PRODUCTION_TYPES,
)
from locations.models import Location
from locations.serializers import LocationSerializer
from productions.serializers import (
    ProductionSerializer,
    ProductionListSerializer,
    SceneSerializer,
    ResearchSerializer,
)


class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all().order_by('-release_date')
    serializer_class = ProductionSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create']:
            return ProductionSerializer
        else: 
            return ProductionListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        order_by = self.request.query_params.get('order_by', '')
        if order_by and order_by in ['title', 'release_date']:
            queryset = queryset.order_by(order_by)

        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        filters = {}

        if 'type' in self.kwargs:
            if self.kwargs['type'] not in [t[0] for t in PRODUCTION_TYPES]:
                raise Http404
            filters['type'] = self.kwargs['type']

        return queryset.filter(**filters)


class SceneLocationViewSet(viewsets.ViewSet):
    def list(self, *args, **kwargs):
        try:
            production = Production.objects.get(slug=kwargs['slug'])
        except Production.DoesNotExist:
            raise Http404

        locations = []

        for location in production.locations.all():
            scenes = location.scene_set.filter(
                production__slug=kwargs['slug']
            )
            locations.append({
                "location": LocationSerializer(location).data,
                "scenes": [SceneSerializer(s).data for s in location.scene_set.filter(
                    production__slug=kwargs['slug']
                )]
            })

        return Response(locations)


# class SceneResearchViewSet(viewsets.ModelViewSet):
#     # queryset = Research.objects.all()
#     serializer_class = ResearchSerializer
#     lookup_field = 'slug'

#     def get_queryset(self):
#         return Research.objects.filter(
#             scenes__production__type=self.kwargs['type'],
#             scenes__production__slug=self.kwargs['slug'],
#         )


class SceneResearchViewSet(viewsets.ViewSet):
    def list(self, *args, **kwargs):
        unidentified_locations = {}

        for scene in Scene.objects.filter(
            production__type=self.kwargs['type'],
            production__slug=self.kwargs['slug'],
            location=None,
        ):
            research = scene.research.first() if scene.research else None
            research_pk = research.pk if research else None
            
            unidentified_locations.setdefault(
                research_pk, {}
            ).setdefault(
                "scenes", []
            ).append(SceneSerializer(scene).data)

            if 'research' not in unidentified_locations[research_pk]:
                research_data = ResearchSerializer(research).data if research else None
                unidentified_locations[research_pk]['research'] = research_data

        return Response(unidentified_locations.values())
