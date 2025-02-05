from django.contrib import admin
from teams.models import Team, TeamCharacter


class TeamAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        members = form.cleaned_data.get("members")
        for member in members:
            TeamCharacter.objects.create(team=obj, character=member)


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamCharacter)
