from django.urls import path
from relics import views

urlpatterns = [
    path("", views.RelicListView.as_view(), name="relics"),
    path("create", views.RelicCreateView.as_view(), name="relic-create"),
    path("<int:relic_id>", views.RelicRetrieveView.as_view(), name="relic-detail"),
    path("<int:relic_id>/edit", views.RelicUpdateView.as_view(), name="relic-edit"),
    path("<int:relic_id>/delete", views.RelicDeleteView.as_view(), name="relic-delete"),
]
