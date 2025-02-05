from rest_framework import serializers
from teams.models import Team, TeamCharacter


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

        def create(self, validated_data):
            members = validated_data.pop("members")
            team = Team.objects.create(**validated_data)
            for member in members:
                TeamCharacter.objects.create(team=team, **member)
            return team


class TeamCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCharacter
        fields = "__all__"
