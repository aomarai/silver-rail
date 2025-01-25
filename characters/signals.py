from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from characters.models import Character
from stats.models import Stat
from characters.default_stats import DEFAULT_STATS

@receiver(post_save, sender=Character)
def assign_default_stats(sender, instance, created, **kwargs):
    if created:  # Only assign stats for newly created characters
        content_type = ContentType.objects.get_for_model(instance)
        Stat.objects.bulk_create([
            Stat(
                stat_type=stat_data['stat_type'],
                stat_category=stat_data['stat_category'],
                value=stat_data['value'],
                content_type=content_type,
                object_id=instance.id
            )
            for stat_data in DEFAULT_STATS
        ])
