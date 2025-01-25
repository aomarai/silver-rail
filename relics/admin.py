from django.contrib import admin
from relics.models import Relic


@admin.register(Relic)
class RelicAdmin(admin.ModelAdmin):
    list_display = ("name", "set_name", "slot", "effect")
    search_fields = ("name", "set_name", "effect")
    list_filter = ("slot", "set_name")
