from django.contrib import admin

import common.models as models


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'uri',)
