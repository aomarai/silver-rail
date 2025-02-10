from django.urls import path
from characters import views

urlpatterns = [
    path("", views.CharacterListView.as_view(), name="characters"),
    path("create/", views.CharacterCreateView.as_view(), name="characters-create"),
    path(
        "<int:pk>/",
        views.CharacterRetrieveView.as_view(),
        name="character-detail",
    ),
    path(
        "<int:pk>/edit/",
        views.CharacterUpdateView.as_view(),
        name="character-edit",
    ),
    path(
        "<int:pk>/delete/",
        views.CharacterDeleteView.as_view(),
        name="character-delete",
    ),
]
