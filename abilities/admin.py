from django.contrib import admin
from abilities.models import Ability


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ("name", "character", "type", "energy_cost", "skill_point_cost")
    search_fields = ("name", "character__name")
    list_filter = ("type",)
