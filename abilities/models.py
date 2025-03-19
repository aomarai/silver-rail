import os

from django.db import models
from django.db.models import Model
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from utils.mixins import HashedFileModelMixin, TimeStampedModelMixin
from utils.model_utils import register_file_cleanup_signals


def ability_main_image_path(instance, filename):
    """Upload path for the main ability image (used in Ability model)"""
    character_name = slugify(instance.character.name)
    character_path = slugify(instance.character.path)
    ability_type = slugify(instance.type)
    extension = filename.split(".")[-1]
    return os.path.join(
        "characters",
        character_path,
        character_name,
        "abilities",
        f"{ability_type}.{extension}",
    )


def ability_image_path(instance, filename):
    """Upload path for alternate ability images (used in AbilityImage model)"""
    character_name = slugify(instance.ability.character.name)
    ability_name = slugify(instance.ability.name)
    ability_type = slugify(instance.ability.type)
    image_type = instance.type
    extension = filename.split(".")[-1]
    return os.path.join(
        "characters",
        character_name,
        "abilities",
        f"{ability_type}-{ability_name}-{image_type}.{extension}",
    )


class Ability(TimeStampedModelMixin, Model):
    ABILITY_TYPES = [
        ("basic", "Basic Attack"),
        ("skill", "Skill"),
        ("talent", "Talent"),
        ("ultimate", "Ultimate"),
        ("technique", "Technique"),
    ]

    TARGETING_TYPES = [
        ("self", "Self"),
        ("ally", "Single Ally"),
        ("allies", "All Allies"),
        ("single", "Single Target"),
        ("blast", "Blast"),
        ("aoe", "Area of Effect"),
    ]

    character = models.ForeignKey(
        "characters.Character", on_delete=models.CASCADE, related_name="abilities"
    )
    name = models.CharField(max_length=128)
    image = models.ImageField(
        upload_to=ability_main_image_path, blank=True, null=True
    )  # Main ability image
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

    class Meta:
        verbose_name = "Ability"
        verbose_name_plural = "Abilities"


class AbilityImage(TimeStampedModelMixin, Model):
    IMAGE_TYPES = [
        ("basic", "Basic Attack"),
        ("skill", "Skill"),
        ("talent", "Talent"),
        ("ultimate", "Ultimate"),
        ("technique", "Technique"),
    ]

    ability = models.ForeignKey(
        Ability, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=ability_image_path)
    type = models.CharField(max_length=16, choices=IMAGE_TYPES, default="basic")

    def __str__(self):
        return f"{self.ability.name} - {self.get_type_display()} Image"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ability Image"
        verbose_name_plural = "Ability Images"


register_file_cleanup_signals(Ability, ["image"])
register_file_cleanup_signals(AbilityImage, ["image"])
