from django.db import models
from django.db.models import Model

class Lightcone(Model):
    name = models.CharField(max_length=128)
    rarity = models.PositiveSmallIntegerField()
    ability = models.CharField(max_length=2048)
    path = models.CharField(max_length=24)

    def __str__(self):
        return self.name