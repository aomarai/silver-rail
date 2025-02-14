from django.db import models
from django.db.models import Model
from rest_framework.exceptions import ValidationError


class Relic(Model):
    SLOTS = [
        ("head", "Head"),
        ("hands", "Hands"),
        ("chest", "Chest"),
        ("feet", "Shoes"),
        ("orb", "Orb"),
        ("rope", "Rope"),
    ]

    name = models.CharField(max_length=128)
    image_url = models.URLField(max_length=2048, blank=True)
    set_name = models.CharField(max_length=128)
    effect = models.CharField(max_length=2048)
    slot = models.CharField(max_length=24, choices=SLOTS)

    def __str__(self):
        return self.name

    def clean(self):
        if self.slot not in dict(self.SLOTS):
            raise ValidationError(f"Invalid slot: {self.slot}")
        if not self.name.strip():
            raise ValidationError("Name cannot be empty")
        if not self.set_name.strip():
            raise ValidationError("Set name cannot be empty")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
