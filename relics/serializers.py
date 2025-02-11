from rest_framework import serializers

from relics.models import Relic


class RelicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relic
        fields = "__all__"
