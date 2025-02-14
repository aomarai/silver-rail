from rest_framework import serializers

from lightcones.models import Lightcone


class LightconeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lightcone
        fields = ["name", "image_url", "path", "rarity", "ability"]
