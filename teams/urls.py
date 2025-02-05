from django.urls import path
from teams import views

urlpatterns = [
    path("", views.index, name="teams-index"),
    path("create/", views.TeamCreateView.as_view(), name="teams-create"),
    path(
        "<int:team_id>/",
        views.TeamRetrieveUpdateDestroyView.as_view(),
        name="team-detail",
    ),
    path(
        "<int:team_id>/edit/",
        views.TeamRetrieveUpdateDestroyView.as_view(),
        name="team-edit",
    ),
    path(
        "<int:team_id>/delete/",
        views.TeamRetrieveUpdateDestroyView.as_view(),
        name="team-delete",
    ),
]
