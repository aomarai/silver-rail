from django.urls import path, include
from rest_framework.routers import DefaultRouter

from relics.views import RelicViewSet

router = DefaultRouter()
router.register(r"relic", RelicViewSet)

urlpatterns = [path("", include(router.urls))]
