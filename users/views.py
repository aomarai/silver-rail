from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.throttlers import RegistrationThrottle
from users.serializers import UserSerializer
from users.models import SilverRailUser


class RegisterView(generics.CreateAPIView):
    queryset = SilverRailUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    throttle_classes = [RegistrationThrottle]
    throttle_scope = "registration"

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "You are already registered."}, status=400)
        return super().post(request, *args, **kwargs)
