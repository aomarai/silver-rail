from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

    def validate(self, data):
        if not data.get('email'):
            raise serializers.ValidationError({'email': 'Email is required'})
        if not data.get('username'):
            raise serializers.ValidationError({'username': 'Username is required'})
        if not data.get('password'):
            raise serializers.ValidationError({'password': 'Password is required'})
        return data