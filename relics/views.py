from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from relics.models import Relic
from relics.serializers import RelicSerializer


class RelicViewSet(viewsets.ModelViewSet):
    queryset = Relic.objects.all()
    serializer_class = RelicSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
