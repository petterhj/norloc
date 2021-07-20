from django.conf import settings
from django.contrib import admin
from leaflet.admin import LeafletGeoAdminMixin, LeafletGeoAdmin, LeafletWidget
from leaflet_admin_list.admin import LeafletAdminListMixin
from django.contrib.gis.db import models as geo_models
from django.utils.html import format_html
from django.urls import reverse

import locations.models as models


LEAFLET_WIDGET_ATTRS = {
    'map_height': '300px',
    'map_width': '100%',
    'display_raw': 'true',
    'map_srid': 4326,
}

LEAFLET_FIELD_OPTIONS = {'widget': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS)}

FORMFIELD_OVERRIDES = {
    geo_models.PointField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiPointField: LEAFLET_FIELD_OPTIONS,
    geo_models.LineStringField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiLineStringField: LEAFLET_FIELD_OPTIONS,
    geo_models.PolygonField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiPolygonField: LEAFLET_FIELD_OPTIONS,
}


@admin.register(models.Location)
class LocationAdmin(LeafletAdminListMixin, LeafletGeoAdminMixin, admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES
    list_display = (
        'name', 'get_municipality_name', 'get_county',
        'ssr_id', 'get_area',
        'slug',
    )
    list_filter = [
        'municipality__county', 'municipality__name',
        'name_types'
    ]
    fieldsets = (
        ('Sentralt stedsnavnregister (SSR)', {
            'fields': ('ssr_id', 'name_types',),
        }),
        ('Locality', {
            'fields': ('name', 'municipality', 'place',),
        }),
        ('Description', {
            'fields': ('description_md',),
        }),
        ('Geometry', {
            'fields': ('geometry',),
        }),
    )

    def get_area(self, obj):
        print("=-" * 10)
        print(obj.geometry, type(obj.geometry))
        print(obj.geometry.area, type(obj.geometry.area))
        print("--" * 10)
        obj.geometry.transform(25832, clone=False)
        print(obj.geometry.area, type(obj.geometry.area))
        return obj.geometry.area
    get_area.short_description = 'Area'

    def get_municipality_name(self, obj):
        return obj.municipality.name
    get_municipality_name.short_description = 'Municipality'

    def get_county(self, obj):
        return obj.municipality.get_county_display()
    get_county.short_description = 'County'

    def get_geojson_feature_line_style(self, request, name, o, queryset):
        return settings.LEAFLET_ADMIN_LIST['line_style']


@admin.register(models.Municipality)
class MunicipalityAdmin(LeafletGeoAdmin):
    list_display = ('name', 'county',)


@admin.register(models.NameType)
class NameTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'slug',)
    fields = ('code', 'name', 'slug', 'description',)
    readonly_fields = ('name', 'slug',)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'location_link', 'has_license', 'created_at',
    )

    def location_link(self, obj):
        return format_html(
            '<a href="{}\" class="changelink">{}</a>',
            reverse("admin:locations_location_change", args=(obj.location.pk,)),
            obj.location,
        )
    location_link.short_description = 'Location'

    def has_license(self, obj):
        return True if obj.license else False
    has_license.boolean = True
    has_license.short_description = 'License'
