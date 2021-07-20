from rest_framework import serializers, viewsets

from common.fields import ChoiceField
from locations.models import (
    Location,
    Photo,
    Municipality,
    NameType,
    NO_COUNTIES,
)


class MunicipalitySerializer(serializers.ModelSerializer):
    county = ChoiceField(choices=NO_COUNTIES)
    county_slug = serializers.SerializerMethodField()
    
    class Meta:
        model = Municipality
        exclude = ('id',)

    def get_county_slug(self, obj):
        return obj.county


class NameTypeSerializer(serializers.ModelSerializer):
    # def validate_code(self, code):
    #     serializers.ValidationError('This field is :(')
    #     return code

    class Meta:
        model = NameType
        exclude = ('id',)# 'code',)
        read_only_fields = ('slug', 'name', 'description',)
        extra_kwargs = {'code': {'validators': []}}


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        # fields = '__all__'
        exclude = ('id', 'location',)


class LocationSerializer(serializers.ModelSerializer):
    name_types = NameTypeSerializer(read_only=False, many=True)
    municipality = MunicipalitySerializer(read_only=False)
    full_address = serializers.CharField(read_only=True)
    photos = PhotoSerializer(source='photo_set', read_only=True, many=True)

    def validate_name_types(self, name_types):
        if not name_types:
            raise serializers.ValidationError('This field is required.')
        return name_types

    def create(self, validated_data):
        name_type_codes = [nt['code'] for nt in validated_data.pop('name_types')]
        name_types = []

        for name_type_code in name_type_codes:
            name_types.append(NameType.objects.get_or_create(
                code=name_type_code,
            )[0])

        validated_data["municipality"] = Municipality.objects.get_or_create(
            **validated_data["municipality"]
        )[0]

        location = Location.objects.create(**validated_data)
        location.name_types.add(*name_types)

        return location

    class Meta:
        model = Location
        # fields = '__all__'
        exclude = ('id', 'description_md',)
        lookup_field = 'slug'
        extra_kwargs = {
            # 'url': {'lookup_field': 'slug', },
        }
    

class LocationListSerializer(LocationSerializer):
    name_types = None
    production_count = serializers.SerializerMethodField()

    class Meta:
        model = Location
        exclude = ('id', 'geometry', 'description_md', 'name_types',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug', }
        }

    def get_production_count(self, obj):
        productions = obj.production_set.all().count()
        return productions
