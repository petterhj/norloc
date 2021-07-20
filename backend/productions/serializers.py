from rest_framework import serializers, viewsets

from productions.models import Production, Scene, Shot, Research
from locations.models import Location
from people.serializers import JobSerializer
from locations.serializers import LocationSerializer


class ProductionSerializer(serializers.ModelSerializer):
    crew = JobSerializer(source='job_set', read_only=True, many=True)
    year = serializers.IntegerField()

    class Meta:
        model = Production
        exclude = ('id', 'locations', 'summary_md',)
        lookup_field = 'slug'
        read_only_fields = ('slug',)


class ProductionListSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    
    class Meta:
        model = Production
        exclude = ('id', 'crew', 'locations', 'summary_md',)
        lookup_field = 'slug'


class ShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shot
        exclude = ('id', 'scene',)


class SceneSerializer(serializers.ModelSerializer):
    shots = ShotSerializer(source='shot_set', read_only=True, many=True)

    class Meta:
        model = Scene
        exclude = (
            'id', 'production', 'location', 'description_md',
        )


class ResearchSerializer(serializers.ModelSerializer):
    # scenes = SceneSerializer(read_only=True, many=True)

    class Meta:
        model = Research
        exclude = ('id', 'description_md', 'scenes',)
