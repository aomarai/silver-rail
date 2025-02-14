from django.db import models
from django.db.models import Model
from rest_framework.exceptions import ValidationError

from characters.models import Character


class Lightcone(Model):
    RARITIES = [(3, "3 Star"), (4, "4 Star"), (5, "5 Star")]

    name = models.CharField(max_length=128)
    image_url = models.URLField(max_length=2048, blank=True, null=True)
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
