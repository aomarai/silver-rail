from django.db import models
from django.db.models import Model
from rest_framework.exceptions import ValidationError

from characters.models import Character

class Team(Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Character, related_name='teams')

    def __str__(self):
        return self.name

    def clean(self):
        if self.members.count() > 4 or self.members.count <= 0:
            raise ValidationError('A team must have one to four members.')