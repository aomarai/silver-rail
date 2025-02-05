from django.urls import path
from characters import views

urlpatterns = [
    path("", views.CharacterListView.as_view(), name="characters"),
    path("create/", views.CharacterCreateView.as_view(), name="characters-create"),
    path(
        "<int:character_id>/",
        views.CharacterRetrieveView.as_view(),
        name="characters-detail",
    ),
    path(
        "<int:character_id>/edit/",
        views.CharacterUpdateView.as_view(),
        name="characters-edit",
    ),
    path(
        "<int:character_id>/delete/",
        views.CharacterDeleteView.as_view(),
        name="characters-delete",
    ),
]
