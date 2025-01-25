from django.db import models
from django.db.models import Model


class Lightcone(Model):
    RARITIES = [(3, "3 Star"), (4, "4 Star"), (5, "5 Star")]

    name = models.CharField(max_length=128)
    rarity = models.PositiveSmallIntegerField(choices=RARITIES)
    ability = models.CharField(max_length=2048)
    path = models.CharField(max_length=24)

    def __str__(self):
        return self.name
