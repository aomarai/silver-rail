from django.urls import path
from characters import views

urlpatterns = [
    path("", views.index, name="characters-index"),
    path("create/", views.CharacterCreateView.as_view(), name="characters-create"),
    path(
        "<int:character_id>/",
        views.CharacterRetrieveView.as_view(),
        name="characters-detail",
    ),
    path(
        "<int:character_id>/edit/",
        views.CharacterRetrieveView.as_view(),
        name="characters-edit",
    ),
    path(
        "<int:character_id>/delete/",
        views.CharacterRetrieveView.as_view(),
        name="characters-delete",
    ),
]
