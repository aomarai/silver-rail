from rest_framework import viewsets
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


from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_storage(request):
    if request.method == "POST" and request.FILES.get("image"):
        file = request.FILES["image"]
        try:
            path = default_storage.save("test/test.jpg", file)
            return JsonResponse(
                {
                    "success": True,
                    "storage_backend": str(default_storage.__class__),
                    "saved_path": path,
                    "full_url": default_storage.url(path),
                }
            )
        except Exception as e:
            return JsonResponse(
                {"error": str(e), "backend": str(default_storage.__class__)}
            )
    return JsonResponse({"status": "ready"})
