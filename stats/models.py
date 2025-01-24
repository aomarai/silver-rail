from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model

class Stat(Model):
    STAT_CATEGORIES = [
        ('base', 'Base Stat'),
        ('advanced', 'Advanced Stat'),
        ('damage', 'Damage Type'),
        ('resistance', 'Resistance Type'),
    ]

    STAT_TYPES = [
        # Base stats
        ('hp', 'HP'),
        ('atk', 'ATK'),
        ('def', 'DEF'),
        ('spd', 'SPD'),

        # Advanced stats
        ('critrate', 'CRIT Rate'),
        ('critdmg', 'CRIT DMG'),
        ('break', 'Break Effect'),
        ('healing', 'Outgoing Healing Boost'),
        ('maxenergy', 'Max Energy'),
        ('energyregen', 'Energy Regeneration Rate'),
        ('effecthit', 'Effect Hit Rate'),
        ('effectres', 'Effect RES'),

        # Damage types
        ('physicalboost', 'Physical DMG Boost'),
        ('fireboost', 'Fire DMG Boost'),
        ('iceboost', 'Ice DMG Boost'),
        ('windboost', 'Wind DMG Boost'),
        ('lightningboost', 'Lightning DMG Boost'),
        ('quantumboost', 'Quantum DMG Boost'),
        ('imaginaryboost', 'Imaginary DMG Boost'),

        # Resistance types
        ('physicalres', 'Physical RES'),
        ('fireres', 'Fire RES'),
        ('iceres', 'Ice RES'),
        ('windres', 'Wind RES'),
        ('lightningres', 'Lightning RES'),
        ('quantumres', 'Quantum RES'),
        ('imaginaryres', 'Imaginary RES'),
    ]

    stat_category = models.CharField(max_length=24, choices=STAT_CATEGORIES)
    stat_type = models.CharField(max_length=24, choices=STAT_TYPES)
    value = models.FloatField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.object} - {self.get_stat_type_display()}"