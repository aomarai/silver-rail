import os

from django.db import models
from django.db.models import Model
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from utils.model_utils import register_file_cleanup_signals


def relic_image_path(instance, filename):
    relic_set_name = slugify(instance.relic.set_name)
    relic_slot = instance.relic.slot
    extension = filename.split(".")[-1]
    return os.path.join(
        "relics",
        relic_set_name,
        f"{relic_slot}.{extension}",
    )


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
    image = models.ImageField(upload_to=relic_image_path, blank=True, null=True)
    set_name = models.CharField(max_length=128)
    effect = models.CharField(max_length=2048, blank=True)
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

register_file_cleanup_signals(Relic, ["image"])