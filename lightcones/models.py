import os

from django.db import models
from django.db.models import Model
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from characters.models import Character


def lightcone_image_path(instance, filename):
    lightcone_name = slugify(instance.lightcone.name)
    lightcone_path = instance.lightcone.path
    image_type = instance.type
    extension = filename.split(".")[-1]
    return os.path.join(
        "lightcones",
        lightcone_path,
        lightcone_name,
        image_type,
        f"{image_type}.{extension}",
    )


class Lightcone(Model):
    RARITIES = [(3, "3 Star"), (4, "4 Star"), (5, "5 Star")]

    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to=lightcone_image_path, blank=True, null=True)
    rarity = models.PositiveSmallIntegerField(choices=RARITIES)
    ability = models.CharField(max_length=2048)
    path = models.CharField(max_length=24, choices=Character.PATHS)

    def __str__(self):
        return self.name

    def clean(self):
        if self.rarity not in dict(self.RARITIES):
            raise ValidationError("Invalid rarity.")
        if not self.name.strip():
            raise ValidationError("Name cannot be empty.")
        if self.path not in dict(Character.PATHS):
            raise ValidationError("Invalid path.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class LightconeImage(Model):
    IMAGE_TYPES = [("full", "Full")]

    lightcone = models.ForeignKey(
        Lightcone, on_delete=models.CASCADE, related_name="images"
    )
    type = models.CharField(max_length=16, choices=IMAGE_TYPES)
    image = models.ImageField(upload_to=lightcone_image_path)

    def __str__(self):
        return f"{self.lightcone.name} - {self.type}"

    def clean(self):
        if self.type not in dict(self.IMAGE_TYPES):
            raise ValidationError("Invalid image type.")
