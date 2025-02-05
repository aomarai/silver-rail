from django.db.models.signals import post_delete
from django.dispatch import receiver

from relics.models import Relic


@receiver(post_delete, sender=Relic)
def remove_relic_from_team_characters(sender, instance, **kwargs):
    for team_character in instance.team_characters.all():
        team_character.relics.remove(instance)
