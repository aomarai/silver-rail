from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from teams.models import Team
from teams.serializers import TeamSerializer


def index(request):
    return render(request, "teams/index.html", {})


class TeamCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        else:
            return Response({"detail": "You are not authenticated."}, status=401)


class TeamRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class TeamListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
