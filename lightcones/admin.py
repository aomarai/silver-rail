from django.contrib import admin
from lightcones.models import Lightcone

@admin.register(Lightcone)
class LightconeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'ability', 'path')
    search_fields = ('name',)
    list_filter = ('rarity', 'path')
