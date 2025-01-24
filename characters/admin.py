from django.contrib import admin
from characters.models import Character, Ability

class AbilityInline(admin.TabularInline):
    model = Ability
    extra = 1

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    inlines = [AbilityInline]
