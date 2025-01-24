from django.db import models
from django.db.models import Model


class Ability(Model):
    ABILITY_TYPES = [
        ('basic', 'Basic Attack'),
        ('skill', 'Skill'),
        ('talent', 'Talent'),
        ('ultimate', 'Ultimate'),
    ]

    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE, related_name='abilities')
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=16, choices=ABILITY_TYPES)
    energy_cost = models.IntegerField(null=True, blank=True) # For ultimates
    skill_point_cost = models.SmallIntegerField(null=True, blank=True) # For skills

    def __str__(self):
        return f"{self.character.name} - {self.name} ({self.get_type_display()})"