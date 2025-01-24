from django.db import models
from django.db.models import Model

class Character(Model):
    TYPES = [
        ('fire', 'Fire'),
        ('ice', 'Ice'),
        ('wind', 'Wind'),
        ('lightning', 'Lightning'),
        ('physical', 'Physical'),
        ('quantum', 'Quantum'),
        ('imaginary', 'Imaginary'),
    ]

    PATHS = [
        ('destruction', 'Destruction'),
        ('hunt', 'The Hunt'),
        ('erudition', 'Erudition'),
        ('harmony', 'Harmony'),
        ('nihility', 'Nihility'),
        ('preservation', 'Preservation'),
        ('abundance', 'Abundance'),
        ('remembrance', 'Remembrance'),
    ]

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=24, choices=TYPES)
    path = models.CharField(max_length=24, choices=PATHS)
    rarity = models.PositiveSmallIntegerField()
    lightcone = models.ForeignKey(
        'lightcones.Lightcone',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters'
    )
    relics = models.ManyToManyField('relics.Relic', related_name='characters')

    def total_stats(self):
        combined_stats = {}

        # Add character base stats
        for stat in self.stats.filter(stat_category='base'):
            combined_stats[stat.stat_type] = combined_stats.get(stat.stat_type, 0) + stat.value

        # Add stats from lightcone
        if self.lightcone:
            for stat in self.lightcone.stats.all():
                combined_stats[stat.stat_type] = combined_stats.get(stat.stat_type, 0) + stat.value

        # Add stats from relics
        for relic in self.relics.all():
            for stat in relic.stats.all():
                combined_stats[stat.stat_type] = combined_stats.get(stat.stat_type, 0) + stat.value

        return combined_stats

    def __str__(self):
        return self.name