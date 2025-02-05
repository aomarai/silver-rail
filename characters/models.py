from django.db import models
from django.db.models import Model


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
    type = models.CharField(max_length=24, choices=TYPES)
    path = models.CharField(max_length=24, choices=PATHS)
    rarity = models.PositiveSmallIntegerField(choices=RARITIES)
    lightcone = models.ForeignKey(
        "lightcones.Lightcone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="characters",
    )
    relics = models.ManyToManyField(
        "relics.Relic", related_name="characters", blank=True
    )

    def __str__(self):
        return self.name
