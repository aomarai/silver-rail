from django.db import models
from django.db.models import Model

from characters.models import Character

class Team(Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Character, related_name='teams')

    def __str__(self):
        return self.name
