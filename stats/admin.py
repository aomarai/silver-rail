from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from stats.models import Stat

class StatInline(GenericTabularInline):
    model = Stat
    extra = 1
    min_num = 0
    verbose_name = "Stat"
    verbose_name_plural = "Stats"

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('get_object', 'get_stat_category', 'get_stat_type', 'value')
    search_fields = ('content_type__model', 'object_id', 'stat_type')
    list_filter = ('stat_category', 'stat_type')

    def get_object(self, obj):
        return f"obj.object.__str__()" # Will show related object, e.g. "Character - 5* Fire Mage"
    get_object.short_description = 'Related Object'

    def get_stat_category(self, obj):
        return obj.get_stat_category_display() # Human-readable category
    get_stat_category.short_description = 'Stat Category'

    def get_stat_type(self, obj):
        return obj.get_stat_type_display()
    get_stat_type.short_description = 'Stat Type'