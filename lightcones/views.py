from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from lightcones.models import Lightcone
from lightcones.serializers import LightconeSerializer


class LightconeViewSet(viewsets.ModelViewSet):
    queryset = Lightcone.objects.all()
    serializer_class = LightconeSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
