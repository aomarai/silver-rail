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

    def total_stats(self):
        # Fetch related data in optimal queries
        character = (
            self.__class__.objects.select_related("lightcone")
            .prefetch_related("stats", "lightcone__stats", "relics__stats")
            .get(id=self.id)
        )

        combined_stats = {}

        # Add character base stats
        for stat in character.stats.filter(stat_category="base"):
            combined_stats[stat.stat_type] = (
                combined_stats.get(stat.stat_type, 0) + stat.value
            )

        # Add stats from lightcone
        if character.lightcone:
            for stat in character.lightcone.stats.all():
                combined_stats[stat.stat_type] = (
                    combined_stats.get(stat.stat_type, 0) + stat.value
                )

        # Add stats from relics
        for relic in character.relics.all():
            for stat in relic.stats.all():
                combined_stats[stat.stat_type] = (
                    combined_stats.get(stat.stat_type, 0) + stat.value
                )

        return combined_stats

    def __str__(self):
        return self.name
