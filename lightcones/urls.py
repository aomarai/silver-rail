from django.urls import path
from lightcones import views

urlpatterns = [
    path("", views.LightconeListView.as_view(), name="lightcones"),
    path("create/", views.LightconeCreateView.as_view(), name="lightcone-create"),
    path("<int:pk>", views.LightconeRetrieveView.as_view(), name="lightcone-detail"),
    path("<int:pk>/edit", views.LightconeUpdateView.as_view(), name="lightcone-edit"),
    path(
        "<int:pk>/delete",
        views.LightconeDestroyView.as_view(),
        name="lightcone-delete",
    ),
]
