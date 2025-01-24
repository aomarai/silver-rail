from django.db import models
from django.db.models import Model

class Relic(Model):
    name = models.CharField(max_length=128)
    set_name = models.CharField(max_length=128)
    effect = models.CharField(max_length=2048)
    slot = models.CharField(max_length=24)

    def __str__(self):
        return self.name