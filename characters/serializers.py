from rest_framework import serializers
from characters.models import Character
from abilities.serializers import AbilitySerializer


class CharacterSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["name", "type", "path", "rarity", "lightcone", "relics"]
