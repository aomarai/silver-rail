from django.urls import path, include
from rest_framework.routers import DefaultRouter

from characters import views

router = DefaultRouter()
router.register(r"characters", views.CharacterViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
