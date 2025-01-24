from rest_framework import serializers
from characters.models import Character, Ability

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['name', 'type', 'description']

class CharacterSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ['name', 'type', 'path', 'rarity', 'lightcone', 'relics']