from django.contrib import admin

import people.models as models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Person', {
            'fields': ('name', 'bio', 'bio_credit',),
        }),
        ('Metadata', {
            'fields': ('tmdb_id', 'imdb_id', 'nbdb_id',),
        }),
    )


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    # pass
    list_display = (
        'get_person_name', 'production', 'type',
    )
    list_filter = (
        'type', 'production__type',
    )

    def get_person_name(self, obj):
        return obj.person.name
    get_person_name.short_description = 'Name'

    # def get_production_title(self, obj):
    #     return obj.production.title
    # get_person_name.short_description = 'Production'
