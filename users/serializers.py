import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import SilverRailUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = SilverRailUser
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return SilverRailUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

    def validate(self, data):
        if not data.get("email"):
            raise serializers.ValidationError({"email": "Email is required."})
        if not data.get("username"):
            raise serializers.ValidationError({"username": "Username is required."})
        if not data.get("password"):
            raise serializers.ValidationError({"password": "Password is required."})
        if SilverRailUser.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        if SilverRailUser.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Username is already in use."}
            )
        try:
            errors = {}
        except ValidationError as e:
            errors["password"] = list(e.messages)
        if errors.get("password"):
            raise serializers.ValidationError(errors)
        return data
