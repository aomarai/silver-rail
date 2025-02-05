from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from characters.models import Character
from characters.serializers import CharacterSerializer


def index(request):
    return render(request, "characters/index.html", {})


class CharacterRetrieveView(generics.RetrieveAPIView):
    queryset = Character.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CharacterSerializer


class CharacterCreateView(generics.CreateAPIView):
    queryset = Character.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CharacterSerializer


class CharacterUpdateView(generics.UpdateAPIView):
    queryset = Character.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CharacterSerializer


class CharacterDeleteView(generics.DestroyAPIView):
    queryset = Character.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CharacterSerializer
