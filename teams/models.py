from django.db import models
from django.db.models import Model
from rest_framework.exceptions import ValidationError

from characters.models import Character


class Team(Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Character, related_name="teams")

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.pk and (self.members.count() > 4 or self.members.count() <= 0):
            raise ValidationError("A team must have 1 to 4 members.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TeamCharacter(Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    character = models.ForeignKey("characters.Character", on_delete=models.CASCADE)
    lightcone = models.ForeignKey(
        "lightcones.Lightcone", on_delete=models.SET_NULL, null=True, blank=True
    )
    relics = models.ManyToManyField(
        "relics.Relic", blank=True, related_name="team_characters"
    )

    # TODO: Implement stats (frontend might be better for this)

    def __str__(self):
        return f"{self.character.name} in {self.team.name}"
