from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

from users.throttlers import RegistrationThrottle
from users.serializers import UserSerializer
from users.models import SilverRailUser


class RegisterView(generics.CreateAPIView):
    queryset = SilverRailUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle]
    throttle_scope = "registration"
