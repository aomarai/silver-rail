from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lightcones.views import LightconeViewSet

router = DefaultRouter()
router.register(r"lightcone", LightconeViewSet)

urlpatterns = [path("", include(router.urls))]
