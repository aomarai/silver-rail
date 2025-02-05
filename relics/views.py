from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from relics.models import Relic
from relics.serializers import RelicSerializer


def index(request):
    return render(request, "relics/index.html", {})


class RelicRetrieveView(generics.RetrieveAPIView):
    queryset = Relic.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RelicSerializer


class RelicCreateView(generics.CreateAPIView):
    queryset = Relic.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = RelicSerializer


class RelicUpdateView(generics.UpdateAPIView):
    queryset = Relic.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = RelicSerializer


class RelicDeleteView(generics.DestroyAPIView):
    queryset = Relic.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = RelicSerializer


class RelicListView(generics.ListAPIView):
    queryset = Relic.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RelicSerializer
