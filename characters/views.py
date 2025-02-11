from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from characters.models import Character
from characters.serializers import CharacterSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
