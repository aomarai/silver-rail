from django.urls import path
from relics import views

urlpatterns = [
    path("", views.RelicListView.as_view(), name="relics"),
    path("create", views.RelicCreateView.as_view(), name="relic-create"),
    path("<int:pk>", views.RelicRetrieveView.as_view(), name="relic-detail"),
    path("<int:pk>/edit", views.RelicUpdateView.as_view(), name="relic-edit"),
    path("<int:pk>/delete", views.RelicDeleteView.as_view(), name="relic-delete"),
]
