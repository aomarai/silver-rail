from django.contrib import admin
from characters.models import Character
from abilities.models import Ability
from .models import Character, CharacterImage


class AbilityInline(admin.TabularInline):
    model = Ability
    extra = 0
    min_num = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    inlines = [AbilityInline]
    list_display = ("name", "rarity", "type")
    search_fields = ("name",)
    list_filter = ("rarity", "type")
    ordering = ("name",)

    def get_inlines(self, request, obj=None):
        return [AbilityInline]


admin.site.register(CharacterImage)
