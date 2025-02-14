from django.db import models
from django.db.models import Model
from rest_framework.exceptions import ValidationError


class Ability(Model):
    ABILITY_TYPES = [
        ("basic", "Basic Attack"),
        ("skill", "Skill"),
        ("talent", "Talent"),
        ("ultimate", "Ultimate"),
        ("technique", "Technique"),
    ]

    TARGETING_TYPES = [
        ("self", "Self"),
        ("ally", "Ally"),
        ("allies", "All Allies"),
        ("single", "Single Target"),
        ("blast", "Blast"),
        ("aoe", "Area of Effect"),
    ]

    character = models.ForeignKey(
        "characters.Character", on_delete=models.CASCADE, related_name="abilities"
    )
    name = models.CharField(max_length=128)
    image_url = models.URLField(max_length=2048, blank=True, null=True)
    type = models.CharField(max_length=16, choices=ABILITY_TYPES)
    energy_cost = models.IntegerField(null=True, blank=True)  # For ultimates
    skill_point_cost = models.SmallIntegerField(null=True, blank=True)  # For skills
    energy_regeneration = models.IntegerField(null=True, blank=True)
    break_effect = models.IntegerField(null=True, blank=True)
    targeting = models.CharField(
        max_length=16, choices=TARGETING_TYPES, default="single"
    )

    def __str__(self):
        return f"{self.character.name} - {self.name} ({self.get_type_display()})"

    def clean(self):
        super().clean()
        if not self.name.strip():
            raise ValidationError("Ability name cannot be empty.")
        if self.type not in dict(self.ABILITY_TYPES):
            raise ValidationError(f"Invalid ability type: {self.type}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
