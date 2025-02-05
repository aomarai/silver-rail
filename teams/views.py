from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from teams.models import Team, TeamCharacter
from teams.serializers import TeamSerializer, TeamCharacterSerializer


class TeamCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        else:
            return Response({"detail": "You are not authenticated."}, status=401)


class TeamUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class TeamDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class TeamRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class TeamListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class TeamCharacterUpdateView(generics.UpdateAPIView):
    # TODO: Lock a lot of these to the specific user
    permission_classes = [IsAuthenticated]
    serializer_class = TeamCharacterSerializer
    queryset = TeamCharacter.objects.all()


class TeamCharacterDestroyView(generics.DestroyAPIView):
    # TODO: Lock a lot of these to the specific user
    permission_classes = [IsAuthenticated]
    serializer_class = TeamCharacterSerializer
    queryset = TeamCharacter.objects.all()


class TeamCharacterRetrieveView(generics.RetrieveAPIView):
    # TODO: Lock a lot of these to the specific user
    permission_classes = [AllowAny]
    serializer_class = TeamCharacterSerializer
    queryset = TeamCharacter.objects.all()
