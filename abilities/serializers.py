from rest_framework import serializers
from abilities.models import Ability


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ["name", "type", "description"]
