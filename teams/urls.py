from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teams import views

router = DefaultRouter()
router.register(r"teams", views.TeamViewSet)
router.register(r"tc", views.TeamCharacterViewSet)

urlpatterns = [path("", include(router.urls))]
