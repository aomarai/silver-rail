from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny

from lightcones.models import Lightcone
from lightcones.serializers import LightconeSerializer


class LightconeCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LightconeSerializer
    queryset = Lightcone.objects.all()


class LightconeRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = LightconeSerializer
    queryset = Lightcone.objects.all()


class LightconeUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LightconeSerializer
    queryset = Lightcone.objects.all()


class LightconeDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LightconeSerializer
    queryset = Lightcone.objects.all()


class LightconeListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LightconeSerializer
    queryset = Lightcone.objects.all()
