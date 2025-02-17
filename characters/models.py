import os
from django.db import models
from django.db.models import Model
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


def character_main_image_path(instance, filename):
    """Upload path for main character image"""
    character_name = slugify(instance.name)
    character_path = slugify(instance.path)
    extension = filename.split(".")[-1]
    return os.path.join("characters", character_path, character_name, f"main.{extension}")


def character_image_path(instance, filename):
    """Upload path for extra character images"""
    character_name = slugify(instance.character.name)
    character_path = slugify(instance.path)
    image_type = instance.type
    extension = filename.split(".")[-1]
    return os.path.join("characters", character_path, character_name, f"{image_type}.{extension}")


class Character(Model):
    TYPES = [
        ("fire", "Fire"),
        ("ice", "Ice"),
        ("wind", "Wind"),
        ("lightning", "Lightning"),
        ("physical", "Physical"),
        ("quantum", "Quantum"),
        ("imaginary", "Imaginary"),
    ]

    PATHS = [
        ("destruction", "Destruction"),
        ("hunt", "The Hunt"),
        ("erudition", "Erudition"),
        ("harmony", "Harmony"),
        ("nihility", "Nihility"),
        ("preservation", "Preservation"),
        ("abundance", "Abundance"),
        ("remembrance", "Remembrance"),
    ]

    RARITIES = [
        (4, "4 Star"),
        (5, "5 Star"),
    ]

    name = models.CharField(max_length=128)
    image = models.ImageField(
        upload_to=character_main_image_path, blank=True, null=True
    )
    type = models.CharField(max_length=24, choices=TYPES)
    path = models.CharField(max_length=24, choices=PATHS)
    rarity = models.PositiveSmallIntegerField(choices=RARITIES)

    def __str__(self):
        return self.name

    def clean(self):
        if self.rarity not in [4, 5]:
            raise ValidationError("Rarity must be either 4 or 5 stars.")
        if self.path not in dict(self.PATHS):
            raise ValidationError("Invalid path.")
        if self.type not in dict(self.TYPES):
            raise ValidationError("Invalid type.")
        if not self.name.strip():
            raise ValidationError("Name cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CharacterImage(Model):
    IMAGE_TYPES = [
        ("full_cg", "Full CG"),
        ("headshot", "Headshot"),
        ("chibi", "Chibi"),
        ("icon", "Icon"),
        ("extra", "Extra"),
    ]

    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=character_image_path)
    type = models.CharField(max_length=16, choices=IMAGE_TYPES, default="extra")

    def __str__(self):
        return f"{self.character.name} - {self.get_type_display()} Image"
