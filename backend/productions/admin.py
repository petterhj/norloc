from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin, LeafletWidget

import productions.models as models


@admin.register(models.Production)
class ProductionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Production', {
            'fields': (
                'type', 'title', 'slug',
                'release_date', 'poster',
                'summary_md', 'runtime',
            ),
        }),
        ('Metadata', {
            'fields': ('tmdb_id', 'imdb_id', 'nbdb_id',),
        }),
    )
    readonly_fields = ('slug',)
    list_display = (
        'title', 'year', 'tmdb_id', 'imdb_id', 'nbdb_id', 'has_poster',
    )
    # list_editable = ('tmdb_id', 'imdb_id', 'nbdb_id',)
    # ordering = ('title',)

    def has_poster(self, obj):
        return True if obj.poster else False
    has_poster.boolean = True
    has_poster.short_description = 'Poster'


@admin.register(models.Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = (
        'production', 'location', 'is_unidentified',
    )

    def is_unidentified(self, obj):
        return obj.is_unidentified
    is_unidentified.boolean = True
    is_unidentified.short_description = 'Unidentified'


@admin.register(models.Shot)
class ShotAdmin(LeafletGeoAdmin):
    list_display = (
        'get_production_title', 'get_location_name', 'timecode', 'highlight',
    )

    def get_location_name(self, obj):
        return obj.scene.location
    get_location_name.short_description = 'Location'

    def get_production_title(self, obj):
        return obj.scene.production.title
    get_production_title.short_description = 'Production'


@admin.register(models.Research)
class ResearchAdmin(LeafletGeoAdmin):
    list_display = (
        'get_production', 'best_guess', 'get_scene_count',
    )

    def get_scene_count(self, obj):
        return obj.scene_count
    get_scene_count.short_description = 'Scenes'

    def get_production(self, obj):
        scene = obj.scenes.first()
        if not scene:
            return
        return scene.production
    get_production.short_description = 'Production'
