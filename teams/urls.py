from django.urls import path
from teams import views

urlpatterns = [
    path("", views.TeamListView.as_view(), name="teams"),
    path("create/", views.TeamCreateView.as_view(), name="teams-create"),
    path(
        "<int:pk>/",
        views.TeamRetrieveView.as_view(),
        name="team-detail",
    ),
    path(
        "<int:pk>/edit/",
        views.TeamUpdateView.as_view(),
        name="team-edit",
    ),
    path(
        "<int:pk>/delete/",
        views.TeamDestroyView.as_view(),
        name="team-delete",
    ),
    path(
        "tc/<int:pk>",
        views.TeamCharacterRetrieveView.as_view(),
        name="teamcharacter-detail",
    ),
    path(
        "tc/<int:pk>/edit",
        views.TeamCharacterUpdateView.as_view(),
        name="teamcharacter-edit",
    ),
    path(
        "tc/<int:pk>/delete",
        views.TeamCharacterDestroyView.as_view(),
        name="teamcharacter-delete",
    ),
]
